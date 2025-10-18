from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from configs import *
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(App_Config)
CORS(app)
api = Api(app)


from pymongo import MongoClient

uri = App_Config.MONGODB_URI
mongo_client = MongoClient(uri)
db = mongo_client['evalsys_db']

db_evaluations = db['evaluations']
db_students = db['student']
db_faculty = db['faculty']
db_forms = db['forms']
db_dean = db['dean']

from src.resources import *