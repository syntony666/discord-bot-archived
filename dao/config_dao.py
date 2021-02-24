from core.database import Database
from core.exception import DataNotExist


class ConfigDAO:
    def __init__(self):
        self.db = Database('config')

    def set_ban_role(self, role_id: str):
        self.set_config('ban_role', role_id)

    def get_ban_role(self):
        return self.get_config('ban_role')

    def set_config(self, _id: str, value: str):
        if len(self.db.get_data({'_id': _id})) == 0:
            self.db.create_data({
                '_id': _id,
                'value': value
            })
        self.db.update_data({'_id': _id}, {"$set": {"value": value}})

    def get_config(self, _id):
        if len(self.db.get_data({'_id': _id})) == 0:
            raise DataNotExist
        # print(self.db.get_data({'_id': _id})[0])
        return int(self.db.get_data({'_id': _id})[0]['value'])
