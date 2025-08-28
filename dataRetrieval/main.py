from fastapi import FastAPI
from pymongo import MongoClient


app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["tweets_db"]

@app.get("/tweets_antisemitic")
def get_interesting_messages():
    collection = db["tweets_antisemitic"]
    return list(collection.find({}, {"_id": 0}))

@app.get("/tweets_not_antisemitic")
def get_not_interesting_messages():
    collection = db["tweets_not_antisemitic"]
    return list(collection.find({}, {"_id": 0}))