from src import api, Resource
from src.resources.services.sentiment_analysis import Sentiment_Analysis
from flask import request


class Evaluation_Controller(Resource):
    def get(self):
        pass
        
    
    def post(self):
        try:
            post_data = request.get_json()
            
            sentiment_analysis_data = Sentiment_Analysis.get_sentiment_polarity(feedback=post_data['inputs'])
            print(sentiment_analysis_data)
            return sentiment_analysis_data
        except Exception as e:
            print(e)
            return "Error on request", 500
    
api.add_resource(Evaluation_Controller, '/evaluation')