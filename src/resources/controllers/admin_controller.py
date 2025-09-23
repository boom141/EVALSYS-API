from src import api, Resource, db_faculty
from src.resources.services.sentiment_analysis import Sentiment_Analysis
from flask import request
from src.helpers import timestamp
from src.resources.services.overview_service import Overview_Service
from src.helpers import serialize_objectid

class Overview_Controller(Resource):
    def get(self):
        
            enitity_id = request.args.get('id', None)
            
            analytics = Overview_Service.get_analytics(condition=enitity_id)
            
            return analytics, 200
    
    
api.add_resource(Overview_Controller, '/overview')

class Faculty_Controller(Resource):
    def get(self):        
        res = list(db_faculty.find())
        res = [serialize_objectid(data) for data in res]
        
        res = [
                {
                    **{k: v for k, v in data.items() if k not in ['password', 'username']},
                    'data': Overview_Service.get_analytics(data['_id'])
                }
                for data in res
            ]
        
        return res, 200
        

api.add_resource(Faculty_Controller, '/faculty')