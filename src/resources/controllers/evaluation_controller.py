from src import api, Resource, db_evaluations
from src.resources.services.sentiment_analysis import Sentiment_Analysis
from src.resources.services.overview_service import Overview_Service
from flask import request
from src.helpers import timestamp


class Evaluation_Controller(Resource):

        
    def post(self):
        try:
            post_data = request.get_json()
            
            sentiment_analysis_data = Sentiment_Analysis.get_sentiment_polarity(feedback=post_data['feedback']['message'])
            likert_score = Overview_Service.get_inforcards(source=[post_data])
            post_data['feedback']['type'] = sentiment_analysis_data.upper()
            post_data['created_at'] = timestamp()

            if likert_score['normalized_rating'] > 50 and post_data['feedback']['type'] == 'NEGATIVE':
                post_data['unserious'] = True
            else:
                post_data['unserious'] = False
            
            
            if likert_score['normalized_rating'] <= 49 and post_data['feedback']['type'] == 'POSITIVE':
                post_data['unserious'] = True
            else:
                post_data['unserious'] = False
            
                
        
            
            db_evaluations.insert_one(post_data)
            
            return 'Resource added successfully', 200
        except Exception as e:
            print(e)
            return "Error on request", 500
    
api.add_resource(Evaluation_Controller, '/evaluation')

