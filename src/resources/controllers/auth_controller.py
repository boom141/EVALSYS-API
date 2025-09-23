from src import api, Resource, db_faculty
from flask import request

class Auth_Controller(Resource):
    def post(self):
        try:
            post_data = request.get_json()
            
            res = None
            if post_data['username'] == 'admin':
                if post_data['password'] == 'admin':
                    res = {'name': 'Admin', 'role': 'admin'}
            
            return res, 200
        except Exception as e:
            print(e)
            return "Error on request", 500
    
api.add_resource(Auth_Controller, '/auth')