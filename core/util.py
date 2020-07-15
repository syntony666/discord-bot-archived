from pymongo import MongoClient

def getDatabase():
    username = 'syntony666'
    password = 'tony738294'
    return new MongoClient(f'mongodb://{username}:{password}@ds027519.mlab.com:27519/heroku_vfz6lbdq?retryWrites=false').heroku_vfz6lbdq

