from src import db_evaluations, db_students, db_faculty
from src.helpers import serialize_objectid
from bson import ObjectId

class Overview_Service:

    @staticmethod
    def get_inforcards(source):
        strongly_disagree = { 'score': 1, 'count': 0  }
        disagree = { 'score': 2, 'count': 0  }
        neutral = { 'score': 3, 'count': 0  }
        agree = { 'score': 4, 'count': 0  }
        outstanding = { 'score': 5, 'count': 0  }
        
        for items in source:
            for key in items['questionnaire']:
                for data in items['questionnaire'][key]:
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
            'strongly_disagree': {'label': 'Strongly Disagree', 'count': strongly_disagree['count']},
            'disagree': {'label': 'Disagree', 'count': disagree['count']},
            'neutral': {'label': 'Neutral', 'count': neutral['count']},
            'agree': {'label': 'Agree', 'count': agree['count']},
            'outstanding': {'label': 'Outstanding', 'count': outstanding['count']},
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
                sentiment = item["feedback"]["type"].lower()
                message = item["feedback"]["message"].strip()
                timestamp = item["created_at"].split(' ')[0].strip()
                
                if sentiment in sentiment_data:
                    sentiment_data[sentiment]["count"] += 1
                    sentiment_data[sentiment]["feedbacks"].append({'message': message, 'timestamp': timestamp})

            except (KeyError, AttributeError):
                continue
        
        rating = 0
        total_response_answer = 0
        for key in sentiment_data:
            rating += sentiment_data[key]['count'] * sentiment_data[key]['score']
            total_response_answer += sentiment_data[key]['count']

        print(source)
        print(sentiment_data)
        print(rating, total_response_answer, '\n\n')
        
        average_rating = round((rating / total_response_answer), 2)
        normalized_rating = round((average_rating / 3) * 100)
        
        sentiment_data['average_rating'] = average_rating
        sentiment_data['normalized_rating'] = normalized_rating
        
        return sentiment_data
    

    @staticmethod
    def unserious_evaluation(source):
        res_data = []
        unserious_evaluations = [item for item in source if item['unserious']]
        for item in unserious_evaluations:
            likert_score = Overview_Service.get_inforcards(source=[item])
            student = db_students.find_one({'_id':ObjectId(item['student_id'])})
            teacher = db_faculty.find_one({'_id':ObjectId(item['teacher_id'])})
            res_data.append({ 'student_name': student['name'], 'section':student['section'], 'course':student['course'], 'teacher_name':teacher['name'], 'evaluation_rating': likert_score['normalized_rating'], 'sentiment_polarity_result':item['feedback']['type'] })

        return res_data
    
    @staticmethod
    def section_checker(student_id):
        try:
            res = db_students.find_one({'_id': ObjectId(student_id)})
            return serialize_objectid(res)['section']
        except Exception as e:
            return False
        
    
    
    @staticmethod
    def get_analytics(teacher_id=None, section_name=None, school_year=None, semester=None):
        res = list(db_evaluations.find())
        
        res = [serialize_objectid(data) for data in res]
        
        if school_year:
            res = [data for data in res if data['school_year'] == school_year]
        
        if semester:
            res = [data for data in res if data['semester'] == int(semester)]
        
        if teacher_id and section_name:
            res = [data for data in res if data['teacher_id'] == teacher_id and section_name == Overview_Service.section_checker(student_id=data['student_id'])]
        
        if teacher_id and section_name == None:
            res = [data for data in res if data['teacher_id'] == teacher_id]
        
        
        analytics = None
        if res:
        
            info_cards = Overview_Service.get_inforcards(source=res)
            sentiment_data = Overview_Service.analyze_feedback_sentiments(source=res)
            participation_score = round((len(res) / 225) * 100,2)
            unserious_evaluation_data = Overview_Service.unserious_evaluation(source=res)
            
            analytics =  { 
                    'info_cards': info_cards,
                    'sentiment_data' : sentiment_data,
                    'participation_score': participation_score,
                    'evaluation_rating': info_cards['normalized_rating'],
                    'feedback_rating': sentiment_data['normalized_rating'],
                    'unserious_evaluation_data': unserious_evaluation_data,
                    'total_response': len(res),
                }
        else:
            analytics = {
                    'evaluation_rating': 0.00,
                    'feedback_rating': 0.00,
                    'total_response': len(res),
                    }
        
        return analytics