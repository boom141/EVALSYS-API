from src import api, Resource, db_faculty, db_evaluations
from src.resources.services.sentiment_analysis import Sentiment_Analysis
from flask import request
from src.helpers import timestamp
from src.resources.services.overview_service import Overview_Service
from src.helpers import serialize_objectid

class Overview_Controller(Resource):
    def get(self):
        
            analytics = Overview_Service.get_analytics()
            
            return analytics, 200
    
api.add_resource(Overview_Controller, '/overview')

class Department_Controller(Resource):
    def get(self):   
        
        sections = ['section_1']
             
        db_res_faculty = list(db_faculty.find())
        db_res_faculty = [serialize_objectid(data) for data in db_res_faculty]
        
        
        faculty_data = [
                {
                    **{k: v for k, v in data.items() if k not in ['password', 'username']},
                    'section_data': [ { 'name': section_name, 'data': Overview_Service.get_analytics(teacher_id=data['_id'], section_name=section_name)} for section_name in sections],
                    'overall_data': Overview_Service.get_analytics(teacher_id=data['_id'])
                }
                for data in db_res_faculty
            ]
        
        # temp_res = []
        # for data in faculty_data:
        #     evaluation_rating_sum = 0
        #     feedback_rating_sum = 0
        #     total_response = 0
        #     for item in data['section_data']:
        #         evaluation_rating_sum += (item['data']['evaluation_rating'] * item['data']['total_response'])
        #         feedback_rating_sum += (item['data']['feedback_rating'] * item['data']['total_response'])
        #         total_response += item['data']['total_response']
    
            
        #     if total_response != 0:
        #         evaluation_rating_avg = evaluation_rating_sum / total_response
        #         feedback_rating_avg = feedback_rating_sum / total_response
        #     else:
        #         evaluation_rating_avg = evaluation_rating_sum 
        #         feedback_rating_avg = feedback_rating_sum
            
        #     temp_res.append({
        #         **data, 
        #         'evaluation_rating': evaluation_rating_avg,
        #         'feedback_rating': feedback_rating_avg,
        #         'total_response': total_response,
        #     })
        
        # faculty_data = temp_res
        
        departments = ['College Of Computing Studies']
        
        temp_res = []
        for department_name in departments:
            department_faculty_data = []      
            evaluation_rating_sum = 0
            feedback_rating_sum = 0
            total_response = 0
            
            for data in faculty_data:
                if data['department'] == department_name:
                    evaluation_rating_sum += ( data['overall_data']['evaluation_rating'] * data['overall_data']['total_response'] )
                    feedback_rating_sum += ( data['overall_data']['feedback_rating'] * data['overall_data']['total_response'] )
                    total_response += data['overall_data']['total_response']
                    department_faculty_data.append(data)

            if total_response != 0:
                evaluation_rating_avg = evaluation_rating_sum / total_response
                feedback_rating_avg = feedback_rating_sum / total_response
            else:
                evaluation_rating_avg = evaluation_rating_sum 
                feedback_rating_avg = feedback_rating_sum
            
            
            temp_res.append({
                'dapartment_name': department_name,
                'evaluation_rating': evaluation_rating_avg,
                'feedback_rating': feedback_rating_avg,
                'total_response': total_response,
                'department_data': department_faculty_data
            })
        
        res = temp_res
        
        return res, 200
        
api.add_resource(Department_Controller, '/department')

