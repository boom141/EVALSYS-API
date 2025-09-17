from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

class App_Config:
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGODB_URI = os.getenv('MONGODB_URI')
    SENTIMENT_ANALYSIS_API = os.getenv('SENTIMENT_ANALYSIS_API')
    OPENAI_API = os.getenv('OPENAI_API')
    HF_ACCESS_TOKEN = os.getenv('HF_ACCESS_TOKEN')