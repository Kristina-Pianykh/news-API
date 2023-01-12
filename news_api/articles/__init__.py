from .controller import router
import os
from pymongo import MongoClient


connection_string = os.environ["DB_CONNECTION_STRING"]
# connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db = client.local
news = db.news
