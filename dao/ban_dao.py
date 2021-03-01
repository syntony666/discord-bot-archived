from bson import ObjectId

from core.database import Database
from core.exception import DataExist, DataNotExist
from core.extension import Extension
from helper.parse_helper import parse_time_duration


class BanDAO:
    def __init__(self):
        self.db = Database('ban')

    def create_ban(self, member_id, start_time, duration, reason):
        end_time = start_time + parse_time_duration(duration)
        for ban in self.db.get_data({"member_id": member_id}):
            if ban['start_time'] + parse_time_duration(ban['duration']) > end_time:
                raise DataExist
        if end_time:
            self.db.create_data({
                "member_id": member_id,
                "start_time": start_time,
                "end_time": start_time + parse_time_duration(duration),
                "duration": duration,
                "reason": reason,
                "unban": False
            })

    def get_ban(self, member_id=None, time=None, unban=None):
        data = dict()
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

    def update_ban(self, objId, duration=None, unban=None, reason=None):
        data = dict()
        start_time = self.db.get_data({"_id": ObjectId(objId)})[0]['start_time']
        if duration is not None:
            data['end_time'] = start_time + parse_time_duration(duration)
        if unban is not None:
            data['unban'] = unban
        if reason is not None:
            data['reason'] = reason
        if bool(data):
            self.db.update_data(
                {"_id": ObjectId(objId)}, {"$set": data})

    def del_ban(self, objId):
        if len(self.db.get_data({"_id": ObjectId(objId)})) == 0:
            raise DataNotExist
        self.db.del_data({"_id": ObjectId(objId)})
