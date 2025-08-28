from pymongo import MongoClient
import os
from dotenv import load_dotenv
from config import  env_path

class MongoConnection:
    @staticmethod
    def _get_uri():
        load_dotenv(dotenv_path=env_path)
        username = os.getenv("db_username")
        password = os.getenv("password")
        uri = f"mongodb+srv://{username}:{password}@cluster0.6ycjkak.mongodb.net/"
        return uri

    @staticmethod
    def _test_connection(connection):
        try:
            connection.admin.command('ping')
            return  True
        except:
            return False

    @staticmethod
    def get_connectin():
        uri = MongoConnection._get_uri()
        connection = MongoClient(uri)
        test = MongoConnection._test_connection(connection)
        if test:
            return connection
        else:
            print("problem in mongo server connectin")
            return None




