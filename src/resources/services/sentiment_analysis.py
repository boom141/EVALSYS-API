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
        
    
    def translate_to_english(feedback):
        content = f"{feedback} {App_Config.TRANSLATOR_COMMAND}"
        return Sentiment_Analysis.language_model(content=content)
        
    @staticmethod
    def get_sentiment_polarity(feedback):
        try:                      
            
            mutated_feedback = Sentiment_Analysis.translate_to_english(feedback=feedback)
            content = f"{mutated_feedback} {App_Config.SENTIMENT_COMMAND}"
            sentiment = Sentiment_Analysis.language_model(content=content)
            return sentiment
            
        except Exception as e:
            raise e
        
        
        
        