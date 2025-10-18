from src import api, Resource, db_faculty, db_evaluations, db_students
from src.resources.services.sentiment_analysis import Sentiment_Analysis
from flask import request
from src.helpers import timestamp
from src.resources.services.overview_service import Overview_Service
from src.helpers import serialize_objectid
from bson.objectid import ObjectId

class Overview_Controller(Resource):
    def get(self):

        school_year = request.args.get('school_year', None)
        semester = request.args.get('semester', None)
        
        analytics = Overview_Service.get_analytics(school_year=school_year,semester=semester)
        
        return analytics, 200
    
api.add_resource(Overview_Controller, '/overview')

class Department_Controller(Resource):
    def get(self):

        school_year = request.args.get('school_year', None)
        semester = request.args.get('semester', None)
        department_name_filter = request.args.get('department_name', None)

        db_res_faculty = list(db_faculty.find())
        db_res_faculty = [serialize_objectid(data) for data in db_res_faculty]
        
        
        faculty_data = [
                {
                    **{k: v for k, v in data.items() if k not in ['password', 'username']},
                    'section_data': [ { 'name': section_name, 'data': Overview_Service.get_analytics(teacher_id=data['_id'], section_name=section_name, school_year=school_year,semester=semester)} for section_name in data['sections']],
                    'overall_data': Overview_Service.get_analytics(teacher_id=data['_id'], school_year=school_year,semester=semester)
                }
                for data in db_res_faculty
            ]
        
        departments = ['College Of Computing Studies', 'College of Health Sciences', 'College of Education', 'College of Criminal Justice', 'College of Business & Public Administration Management']
        
        temp_res = []
        for department_name in departments:
            department_faculty_data = []      
            evaluation_rating_sum = 0
            feedback_rating_sum = 0
            total_response = 0
            faculty_name = []
            
            for data in faculty_data:
                if data['department'] == department_name and data['_id'] not in faculty_name:
                    evaluation_rating_sum += ( data['overall_data']['evaluation_rating'] * data['overall_data']['total_response'] )
                    feedback_rating_sum += ( data['overall_data']['feedback_rating'] * data['overall_data']['total_response'] )
                    total_response += data['overall_data']['total_response']
                    department_faculty_data.append(data)
                    faculty_name.append(data['name'])

            if total_response != 0:
                evaluation_rating_avg = evaluation_rating_sum / total_response
                feedback_rating_avg = feedback_rating_sum / total_response
            else:
                evaluation_rating_avg = evaluation_rating_sum 
                feedback_rating_avg = feedback_rating_sum
            
            
            temp_res.append({
                'department_name': department_name,
                'evaluation_rating': round(evaluation_rating_avg, 2),
                'feedback_rating': round(feedback_rating_avg, 2),
                'total_response': total_response,
                'department_data': department_faculty_data
            })
        
        res = temp_res
        
        if department_name_filter != None:
            res = [data for data in res if data['department_name'] == department_name_filter]
        
        db_res_students = list(db_students.find())
        db_res_students = [{'name': data['section']} for data in db_res_students]
        
        return {'data': res, 'sections': db_res_students}, 200
    
    def put(self,id):
        update_data = request.get_json()
      
        
        faculty_member = db_faculty.find_one({'_id':ObjectId(id)})

        section_list = list(set(faculty_member['sections'] + update_data['sections']))
                
        db_faculty.update_one(
            {'_id':ObjectId(id)},
            {'$set': {
                'sections':section_list
            }}
        )
        
        for data in update_data['sections']:
            student = db_students.find_one({'section':data})

            evaluatees = list(set(student['evaluatees'] + [str(faculty_member['_id'])]))
                    
            db_students.update_one(
                {'section':data},
                {'$set': {
                    'evaluatees': evaluatees
                }}
            )
        
        return 'Section added successfully', 200
        
        
api.add_resource(Department_Controller, '/department', '/department/faculty/<id>')


