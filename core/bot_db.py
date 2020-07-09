from pymongo import MongoClient

class MongoDB():
    def __init__(self):
        username = 'syntony666'
        password = 'tony738294'
        self.__db = MongoClient(f'mongodb://{username}:{password}@ds027519.mlab.com:27519/heroku_vfz6lbdq?retryWrites=false').heroku_vfz6lbdq

    def auth(self, collection: str):
        auth = self.__db['auth'].find_one()
        return auth[collection]