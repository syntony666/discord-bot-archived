from pymongo import MongoClient

from setting import DATABASE_URL, DATABASE_NAME


class Database:
    def __init__(self):
        self.database = MongoClient(DATABASE_URL).get_database(DATABASE_NAME)

    def _find_data(self, col_name: str, query: dict):
        return self.database.get_collection(col_name).find(query)

    def _create_data(self, col_name: str, query: dict):
        self.database.get_collection(col_name).insert_one(query)

    def _update_data(self, col_name: str, query: dict, data: dict):
        self.database.get_collection(col_name).update_many(query, data)

    def _del_data(self, col_name: str, query: dict):
        self.database.get_collection(col_name).delete_many(query)


