import os
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
        data = self.tweets_collection.find({}).sort("CreateDate",1).skip(self.retrieves_count).limit(100)
        data_list = list(data)
        self.retrieves_count += len(data_list)
        return data_list


