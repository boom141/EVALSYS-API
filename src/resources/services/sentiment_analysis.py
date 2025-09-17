import requests
from configs import App_Config

class Sentiment_Analysis:
    @staticmethod
    def translate_to_english(feedback):
        headers = {
            "Authorization": f"Bearer {App_Config.HF_ACCESS_TOKEN}"
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": f"{feedback} PLEASE TRANSLATE TO ENGLISH"
                }
            ],
            "model": "openai/gpt-oss-20b:nebius"
        }
        
        response = requests.post(App_Config.OPENAI_API, headers=headers, json=payload)
        result =   response.json()
        return result['choices'][0]['message']['content']
        
            
    @staticmethod
    def classify_sentiment(label):
        if label in ["4 stars", "5 stars"]:
            return "Positive"
        elif label == "3 stars":
            return "Neutral"
        else:
            return "Negative"
    
    @staticmethod
    def get_sentiment_polarity(feedback):
        try:          
            headers = {
                "Authorization": f"Bearer {App_Config.HF_ACCESS_TOKEN}",
            }
            
            payload = {
                "inputs": Sentiment_Analysis.translate_to_english(feedback=feedback)
            }
            
            
            response = requests.post(App_Config.SENTIMENT_ANALYSIS_API, headers=headers, json=payload)
            [result] =   response.json()
    
            raw_label = result[0]['label']
            sentiment = Sentiment_Analysis.classify_sentiment(raw_label)
            
            return sentiment
            
        except Exception as e:
            raise e