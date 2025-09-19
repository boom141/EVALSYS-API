from src import db_evaluations
from src.helpers import serialize_objectid

class Overview_Service:

    @staticmethod
    def get_inforcards(source):
        strongly_disagree = { 'score': 1, 'count': 0  }
        disagree = { 'score': 2, 'count': 0  }
        neutral = { 'score': 3, 'count': 0  }
        agree = { 'score': 4, 'count': 0  }
        outstanding = { 'score': 5, 'count': 0  }
        
        for items in source:
            for key in items['questionaire']:
                for data in items['questionaire'][key]:
                    if data['score'] == strongly_disagree['score']:
                        strongly_disagree['count'] += 1
                    if data['score'] == disagree['score']:
                        disagree['count'] += 1
                    if data['score'] == neutral['score']:
                        neutral['count'] += 1
                    if data['score'] == agree['score']:
                        agree['count'] += 1
                    if data['score'] == outstanding['score']:
                        outstanding['count'] += 1
        
        total_response_answer = strongly_disagree['count'] + disagree['count'] + neutral['count'] + agree['count'] + outstanding['count']
        
        average_rating = ((strongly_disagree['score'] * strongly_disagree['count']) + (disagree['score'] 
            * disagree['count']) + (neutral['score'] * neutral['count']) + (agree['score'] * 
            agree['count']) + (outstanding['score'] * outstanding['count'])) / total_response_answer
        
        average_rating = round(average_rating, 2)
        normalized_rating = round(((average_rating / 5) * 100), 2)
        
        return {
            'strongly_disagree': {'label': 'Strongly Disagree', 'count': strongly_disagree},
            'disagree': {'label': 'Disagree', 'count': disagree},
            'neutral': {'label': 'Neutral', 'count': neutral},
            'agree': {'label': 'Agree', 'count': agree},
            'outstanding': {'label': 'Outstanding', 'count': outstanding},
            'average_rating': average_rating,
            'normalized_rating': normalized_rating
        }
    
    @staticmethod
    def analyze_feedback_sentiments(source):
        sentiment_data = {
            "positive": {
                "score": 3,
                "count": 0,
                "feedbacks": []
            },
            "neutral": {
                "score": 2,
                "count": 0,
                "feedbacks": []
            },
            "negative": {
                "score": 1,
                "count": 0,
                "feedbacks": []
            }
        }

        for item in source:
            try:
                sentiment = item["feedback"]["type"].strip().lower()
                message = item["feedback"]["message"].strip()

                if sentiment in sentiment_data:
                    sentiment_data[sentiment]["count"] += 1
                    sentiment_data[sentiment]["feedbacks"].append(message)

            except (KeyError, AttributeError):
                continue
        
        rating = 0
        total_response_answer = 0
        for key in sentiment_data:
            rating += sentiment_data[key]['count'] * sentiment_data[key]['score']
            total_response_answer += sentiment_data[key]['count']
        
        average_rating = round((rating / total_response_answer), 2)
        normalized_rating = round((average_rating / 3) * 100)
        
        sentiment_data['average_rating'] = average_rating
        sentiment_data['normalized_rating'] = normalized_rating
        
        return sentiment_data
        
    
    @staticmethod
    def get_analytics(condition):
        res = list(db_evaluations.find())
        
        res = [serialize_objectid(data) for data in res]
        
        if condition:
            res = [data for data in res if data['teacher_id'] == condition]
        
        
        info_cards = Overview_Service.get_inforcards(source=res)
        sentiment_data = Overview_Service.analyze_feedback_sentiments(source=res)
        participation_score = round((len(res) / 350) * 100,2)
    
        
        analytics =  { 
                'info_cards': info_cards,
                'sentiment_data' : sentiment_data,
                'participation_score': participation_score,
                'total_response': len(res),
            }
        
        return analytics