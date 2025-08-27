from pymongo import MongoClient
import os
from dotenv import load_dotenv
from config import  env_path
from mongo_connection import  MongoConnection

class Dal:
    def __init__(self):
        self.tweets_collection = self._init_collection()

    def _init_collection(self):
        connection = MongoConnection.get_connectin()
        db_name = os.getenv("DBname")
        collection_name = os.getenv("collection_name")
        db = connection[db_name]
        collection = db[collection_name]
        return collection

    def get_data(self):
        data = self.tweets_collection.find({},{"_id":0})
        return list(data)

d = Dal()
s = d.get_data()
print(s)
