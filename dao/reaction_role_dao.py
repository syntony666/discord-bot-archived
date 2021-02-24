import discord

from core.database import Database
from core.exception import DataExist, DataNotExist


class ReactionRoleDAO:
    def __init__(self):
        self.db = Database('reaction_role')

    def create_rr(self, role_id, message_id, emoji: discord.Emoji):
        if len(self.db.get_data({"_id": role_id})) == 0:
            self.db.create_data({
                "_id": role_id,
                "message_id": message_id,
                "emoji": emoji
            })
        else:
            raise DataExist

    def get_rr(self, role_id=None, message_id=None, emoji=None):
        if role_id is None and message_id is None and emoji is None:
            return self.db.get_data({})
        data = dict()
        if role_id is not None:
            data['_id'] = role_id
        if message_id is not None:
            data['message_id'] = message_id
        if emoji is not None:
            data['emoji'] = emoji
        if len(self.db.get_data(data)) == 0:
            return None
        return self.db.get_data(data)[0]

    def update_rr(self, role_id, message_id=None, emoji=None):
        if len(self.db.get_data({"_id": role_id})) == 0:
            raise DataNotExist
        data = dict()
        if message_id is not None:
            data['message_id'] = message_id
        if emoji is not None:
            data['emoji'] = emoji
        return self.db.update_data({"_id": role_id}, {"$set": data})

    def del_rr(self, role_id=None, message_id=None):
        data = dict()
        if message_id is not None:
            data['message_id'] = message_id
        if role_id is not None:
            data['emoji'] = role_id
        if len(self.db.get_data(data)) == 0:
            raise DataNotExist
        return self.db.del_data(data)
