from src import api, Resource, db_faculty, db_students
from flask import request
from src.helpers import timestamp
from src.helpers import serialize_objectid
from bson.objectid import ObjectId

class Student_Controller(Resource):
    def get(self):
        try:
            student_id = request.args.get('student_id', False)
            print(student_id)
            student_res = list(db_students.find())
            student_res = [serialize_objectid(data) for data in student_res if str(data['_id']) == student_id]
            print(student_res)
            
            faculties = [ data['teacher_id'] for data in student_res[0]['evaluatees'] ]
                
            faculty_res = list(db_faculty.find())
            faculty_res = [serialize_objectid(data) for data in faculty_res]


            faculty_res = [
                    {
                        **{k: v for k, v in data.items() if k not in ['password', 'username']},
                    }
                    for data in faculty_res
                    if data['_id'] in faculties
                ]
            
            
            return faculty_res, 200
        except Exception as e:
            print(e)
            return "Error on request", 500
        
api.add_resource(Student_Controller, '/student')