from core.database import Database
from core.exception import DataExist, DataNotExist
from helper.parse_helper import DurationParser


class BanDAO:
    def __init__(self):
        self.db = Database('ban')

    def create_ban(self, member_id, start_time, duration, reason):
        end_time = start_time + DurationParser(duration).get_time()
        if self.get_ban(member_id=member_id, unban= True) is not None:
            raise DataExist
        if end_time:
            self.db.create_data({
                "_id": f'{member_id}{start_time.strftime("%Y%m%d%H%M%S")}',
                "member_id": str(member_id),
                "start_time": start_time,
                "end_time": start_time + DurationParser(duration).get_time(),
                "duration": duration,
                "reason": reason,
                "unban": False
            })

    def get_ban(self, _id=None, member_id=None, time=None, unban=None):
        data = dict()
        if _id is not None:
            data['_id'] = str(_id)
        if member_id is not None:
            data['member_id'] = str(member_id)
        if time is not None:
            data['start_time'] = {'$lt': time}
            data['end_time'] = {'$gte': time}
        if unban is not None:
            data['unban'] = unban
        if len(self.db.get_data(data)) == 0:
            return None
        return self.db.get_data(data)

    def update_ban(self, _id, duration=None, unban=None, reason=None):
        data = dict()
        start_time = self.db.get_data({"_id": _id})[0]['start_time']
        if duration is not None:
            data['end_time'] = start_time + DurationParser(duration).get_time()
        if unban is not None:
            data['unban'] = unban
        if reason is not None:
            data['reason'] = reason
        if bool(data):
            self.db.update_data(
                {"_id": _id}, {"$set": data})

    def del_ban(self, _id):
        if len(self.db.get_data({"_id": _id})) == 0:
            raise DataNotExist
        self.db.del_data({"_id": _id})
