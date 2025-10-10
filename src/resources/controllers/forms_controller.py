from src import api, Resource, db_forms
from flask import request
from src.helpers import serialize_objectid, timestamp
from bson.objectid import ObjectId

class Forms_Controller(Resource):
    def get(self):
        try:
            res = list(db_forms.find())
            res = [serialize_objectid(item) for item in res]
            
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
            
            db_forms.update_one(
                {'_id': ObjectId(id)},
                {'$set': update_data}
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