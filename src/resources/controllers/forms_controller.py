from src import api, Resource, db_forms
from flask import request
from src.helpers import serialize_objectid, timestamp
from bson.objectid import ObjectId

class Forms_Controller(Resource):
    def get(self):
        try:
            role = request.args.get('role', None)
            school_year = request.args.get('school_year', None)
            semester = request.args.get('semester', None)
            
            if role == 'student':
                res = db_forms.find_one({'status': 'Active'})
                res['_id'] = str(res['_id'])
                return res
            
            
            res = list(db_forms.find())
            res = [serialize_objectid(item) for item in res]
            
                    
            if school_year:
                res = [data for data in res if data['school_year'] == school_year]
            
            if semester:
                res = [data for data in res if data['semester'] == int(semester)]
            
            return res, 200
        
        except Exception as e:
            print(e)
            return "Error on request", 500
        
        
    def post(self):
        try:
            post_data = request.get_json()
            post_data['created_at'] = timestamp()
            
            db_forms.insert_one(post_data)

            return 'Resource added successfully', 200
        except Exception as e:
            print(e)
            return "Error on request", 500
        
    def put(self, id):
        try:
            update_data = request.get_json()

            db_forms.update_many(
                {'status': {'$eq':'Active'}},
                {'$set':{'status':'Inactive'}}
            )
            
            db_forms.update_one(
                {'_id': ObjectId(id)},
                {'$set': update_data['update_data']}
            )
            
            return 'Resource updated successfully', 200
        except Exception as e:
            print(e)
            return "Error on request", 500
        
    def delete(self, id):
        try:
            db_forms.delete_one({'_id': ObjectId(id)})
            
            return 'Resource deleted successfully', 200
        except Exception as e:
            print(e)
            return "Error on request", 500
    
api.add_resource(Forms_Controller, '/forms', '/forms/<id>')