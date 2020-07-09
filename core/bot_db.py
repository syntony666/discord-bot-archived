from pymongo import MongoClient

class MongoDB():
    def __init__(self):
        print('init db')
        username = 'syntony666'
        password = 'tony738294'
        self.__db = MongoClient(f'mongodb://{username}:{password}@ds027519.mlab.com:27519/heroku_vfz6lbdq?retryWrites=false').heroku_vfz6lbdq
        print('init finished')
    def auth(self, collection: str):
        print(f'{collection} auth called')
        auth = self.__db['auth'].find_one()
        print(auth)
        return auth[collection]