from src import api, Resource, db_evaluations
from src.resources.services.sentiment_analysis import Sentiment_Analysis
from flask import request
from src.helpers import timestamp


class Evaluation_Controller(Resource):
        
    def post(self):
        try:
            post_data = request.get_json()
            
            sentiment_analysis_data = Sentiment_Analysis.get_sentiment_polarity(feedback=post_data['feedback']['message'])
            post_data['feedback']['type'] = sentiment_analysis_data
            post_data['created_at'] = timestamp()
            
            db_evaluations.insert_one(post_data)
            
            return 'Resource added successfully', 200
        except Exception as e:
            print(e)
            return "Error on request", 500
    
api.add_resource(Evaluation_Controller, '/evaluation')

