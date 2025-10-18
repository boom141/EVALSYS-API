from src import api, Resource, db_faculty, db_students, db_dean
from flask import request
from src.helpers import serialize_objectid


class Auth_Controller(Resource):
    def post(self):
        try:
            post_data = request.get_json()
    
            if post_data['username'] == 'admin':
                if post_data['password'] == 'admin':
                    return {'name': 'Admin', 'role': 'admin'}, 200
            
            res = db_dean.find_one({'username': post_data['username']})
            if res:
                res = serialize_objectid(res)
                if post_data['password'] == res['password']:
                    return   {
                    **{k: v for k, v in res.items() if k not in ['password', 'username']},
                    }
            
            res = db_faculty.find_one({'username':post_data['username']})
            if res:
                res = serialize_objectid(res)
                if post_data['password'] == res['password']:
                    return   {
                    **{k: v for k, v in res.items() if k not in ['password', 'username']},
                 
                    }
                    
            res = db_students.find_one({'username':post_data['username']})
            if res:
                res = serialize_objectid(res)
                if post_data['password'] == res['password']:
                    return   {
                    **{k: v for k, v in res.items() if k not in ['password', 'username']},
                 
                    }
                    
                    
            if not res:
                return 'Access Denied', 403
            
        except Exception as e:
            print(e)
            return "Error on request", 500
    
api.add_resource(Auth_Controller, '/auth')