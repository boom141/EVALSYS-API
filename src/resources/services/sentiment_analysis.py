import requests
from configs import App_Config

class Sentiment_Analysis:
    @staticmethod
    def language_model(content):
        headers = {
            "Authorization": f"Bearer {App_Config.HF_ACCESS_TOKEN}"
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f"{content}"
                }
            ],
            "model": "openai/gpt-oss-20b:nebius"
        }
        
        response = requests.post(App_Config.OPENAI_API, headers=headers, json=payload)
        result =  response.json()
        return result['choices'][0]['message']['content']
        
            
    # @staticmethod
    # def classify_sentiment(label):
    #     if label in ["4 stars", "5 stars"]:
    #         return "Positive"
    #     elif label == "3 stars":
    #         return "Neutral"
    #     else:
    #         return "Negative"
    
    def translate_to_english(feedback):
        content = f"{feedback} PLEASE TRANSLATE TO ENGLISH, IF ITS ALREADY IN ENGLISH JUST RETURN THE CONTENT THAT I SENT TO YOU"
        return Sentiment_Analysis.language_model(content=content)
        
    @staticmethod
    def get_sentiment_polarity(feedback):
        try:                      
            
            mutated_feedback = Sentiment_Analysis.translate_to_english(feedback=feedback)
            content = f"{mutated_feedback} GIVE THE SENTIMENT OF THIS CONTENT ONLY SAYS NEGATIVE, NEUTRAL, POSITIVE"
            sentiment = Sentiment_Analysis.language_model(content=content)
            return sentiment
            
        except Exception as e:
            raise e
        
        
        
        