from pymongo import MongoClient
import os

def getDatabase():
    # get variable from heroku var
    username = str(os.environ.get('username'))
    password = str(os.environ.get('password'))
    dbname = str(os.environ.get('dbName'))
    print(os.environ.get('username'))
    # access data from MongoDB
    db = MongoClient(f'mongodb+srv://{username}:{password}@discordbotdb-iopzr.gcp.mongodb.net/{dbname}?retryWrites=true&w=majority')
    return db[dbname]
