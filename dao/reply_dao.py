from core.database import Database
from core.exception import DataExist, DataNotExist


class ReplyDAO:
    def __init__(self):
        self.db = Database('reply')

    def create_reply(self, receive, send):
        if len(self.db.get_data({"_id": receive})) == 0:
            self.db.create_data({
                "_id": receive,
                "value": send
            })
        else:
            raise DataExist

    def get_reply(self, receive=None):
        if receive is None:
            return self.db.get_data({})
        if len(self.db.get_data({"_id": receive})) == 0:
            return None
        return self.db.get_data({"_id": receive})[0]

    def update_reply(self, receive, send):
        if len(self.db.get_data({"_id": receive})) == 0:
            raise DataNotExist
        self.db.update_data(
            {"_id": receive}, {"$set": {"value": send}})

    def del_reply(self, receive):
        if len(self.db.get_data({"_id": receive})) == 0:
            raise DataNotExist
        response = self.db.get_data({"_id": receive})[0]
        self.db.del_data({
            "_id": receive
        })
        if len(self.db.get_data({"_id": receive})) != 0:
            raise DataExist
        return response
