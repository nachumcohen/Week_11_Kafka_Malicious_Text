from pymongo import MongoClient
import os
from dotenv import load_dotenv
from config import  env_path
from mongo_connection import  MongoConnection

class Dal:
    def __init__(self):
        self.tweets_collection = self._init_collection()
        self.retrieves_count = 0

    def _init_collection(self):
        connection = MongoConnection.get_connectin()
        db_name = os.getenv("DBname")
        collection_name = os.getenv("collection_name")
        db = connection[db_name]
        collection = db[collection_name]
        return collection

    def get_data(self):
        data = self.tweets_collection.find({},{"_id":0}).sort("CreateDate",1).skip(100*self.retrieves_count).limit(100)
        self.retrieves_count += 1
        return list(data)


    def _get_collection_size(self):
        meta_data = self.tweets_collection.database.command("collstats", self.tweets_collection.name)
        return meta_data["count"]


    def check_work_finsh(self):
        collection_size = self._get_collection_size()
        if self.retrieves_count*100 < collection_size:
            return True
        print("all collection have been read.... the work finished")
        return False

