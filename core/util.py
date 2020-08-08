from pymongo import MongoClient
import os

def getDatabase():
    # get variable from heroku var
    username = str(os.environ.get('MONGODB_USERNAME'))
    password = str(os.environ.get('MONGODB_PASSWORD'))
    dbname = 'bot-db'
    # access data from MongoDB
    db = MongoClient(f'mongodb+srv://{username}:{password}@discordbotdb-iopzr.gcp.mongodb.net/{dbname}?retryWrites=true&w=majority')
    return db[dbname]
