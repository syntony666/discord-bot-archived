from pymongo import MongoClient

from setting import DATABASE_URL, DATABASE


class Database:
    def __init__(self, col_name: str):
        db_url = DATABASE_URL
        # access data from MongoDB
        self.col = MongoClient(db_url).get_database(DATABASE).get_collection(col_name)

    def get_col(self):
        return self.col
    
    def create_data(self, data):
        self.col.insert_one(data)
    
    def get_data(self, query):
        return [x for x in self.col.find(query)]
    
    def update_data(self, query, data):
        return self.col.update_many(query, data)
        
    def del_data(self, query):
        self.col.delete_many(query)
