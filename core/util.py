from pymongo import MongoClient
import os

def getDatabase():
    # get variable from heroku var
    username = os.environ.get('username')
    password = os.environ.get('password')
    dbname = os.environ.get('dbName')
    # access data from MongoDB
    db = MongoClient(f'mongodb+srv://{username}:{password}@discordbotdb-iopzr.gcp.mongodb.net/{dbname}?retryWrites=true&w=majority')
    return db[str(dbname)]
