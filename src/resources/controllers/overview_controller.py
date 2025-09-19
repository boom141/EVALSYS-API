from src import api, Resource, db_evaluations
from src.resources.services.sentiment_analysis import Sentiment_Analysis
from flask import request
from src.helpers import timestamp
from src.resources.services.overview_service import Overview_Service

class Overview_Controller(Resource):
    def get(self):
        try:
            enitity_id = request.args.get('id', None)
            
            analytics = Overview_Service.get_analytics(condition=enitity_id)
            
            return analytics, 200
        
        except Exception as e:
            print(e)
            return "Error on request", 500
    
        
    
    
    
api.add_resource(Overview_Controller, '/overview')