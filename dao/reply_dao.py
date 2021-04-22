from core.database import Database
from core.exception import DataNotExist, DataExist
from model.reply_model import ReplyModel


class ReplyDao(Database):
    def __init__(self):
        super(ReplyDao, self).__init__()
        self.col_name = 'reply'

    def get_data(self, guild_id: str, receive=None):
        query = dict()
        query['_id.guild'] = guild_id
        if receive is not None:
            query['_id.receive'] = receive
        response = self._find_data(self.col_name, query)
        if response is None:
            return []
        reply = [ReplyModel(guild_id, found['_id']['receive'], found['send'])
                for found in response]
        return reply

    def create_data(self, guild_id: str, receive: str, send: str):
        if len(self.get_data(guild_id, receive)) != 0:
            raise DataExist
        query = dict()
        query['_id'] = {'guild': guild_id, 'receive': receive}
        query['send'] = send
        self._create_data(self.col_name, query)

    def update_data(self, guild_id: str, receive: str, send: str):
        if len(self.get_data(guild_id, receive)) == 0:
            raise DataNotExist
        query = dict()
        query['_id'] = {'guild': guild_id, 'receive': receive}
        data = dict()
        data['$set'] = dict()
        data['$set']['send'] = send
        self._update_data(self.col_name, query, data)

    def del_data(self, guild_id: str, receive: str):
        if len(self.get_data(guild_id, receive)) == 0:
            raise DataNotExist
        query = dict()
        query['_id'] = {'guild': guild_id, 'receive': receive}
        self._del_data(self.col_name, query)
