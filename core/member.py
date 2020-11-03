from datetime import datetime

from core.util import getDatabase


class Member:
    def __init__(self, member_id: int, guild_id: int):
        self.__member_id = member_id
        self.__guild_id = guild_id
        self.__query = {'server': self.__guild_id, 'user': self.__member_id}
        self.__collection = getDatabase().get_collection('member-info')
        self.__data = self.__collection.find_one(self.__query)
        if self.__data is None:
            self.setup_new_member()

    def setup_new_member(self):
        self.__collection.insert_one({
            'server': self.__guild_id,
            'user': self.__member_id,
            'msg-count': 0,
            'level': 0,
            'exp': 0,
            'send-msg-time': datetime.now(),
            'money': 0,
            'daily-money': datetime.now()
        })
        self.__data = self.__collection.find_one(self.__query)

    def get_level(self):
        return self.__data.get('level')

    def set_level(self, level):
        self.__collection.find_one_and_update(self.__query, {
            '$set': {'level': level}
        })
        self.__data = self.__collection.find_one(self.__query)

    def get_exp(self):
        return self.__data.get('exp')

    def add_exp(self, exp: int):
        exp = self.get_exp() + exp
        if exp > self.get_level_exp():
            self.__collection.find_one_and_update(self.__query, {
                '$set': {'level': self.get_level() + 1, 'exp': exp - self.get_level_exp()}
            })
        else:
            self.__collection.find_one_and_update(self.__query, {
                '$set': {'exp': exp}
            })
        self.__data = self.__collection.find_one(self.__query)

    def get_cash(self):
        return self.__data.get('cash')

    def set_cash(self, cash: int):
        self.__collection.find_one_and_update(self.__query, {
            '$set': {'cash': cash}
        })
        self.__data = self.__collection.find_one(self.__query)

    def get_msg_count(self):
        return self.__data.get('msg-count')

    def set_msg_count(self, msg_count: int):
        self.__collection.find_one_and_update(self.__query, {
            '$set': {'cash': msg_count}
        })
        self.__data = self.__collection.find_one(self.__query)

    def get_msg_time(self):
        return self.__data.get('send-msg-time')

    def set_msg_now_time(self):
        self.__collection.find_one_and_update(self.__query, {
            '$set': {'send-msg-time': datetime.now()}
        })
        self.__data = self.__collection.find_one(self.__query)

    def get_daily_cash_time(self):
        return self.__data.get('send-msg-time')

    def set_daily_cash_now_time(self):
        self.__collection.find_one_and_update(self.__query, {
            '$set': {'daily-cash': datetime.now()}
        })
        self.__data = self.__collection.find_one(self.__query)

    def get_level_exp(self):
        return 5 * self.get_level() ** 2 + (50 * self.get_level()) + 100

    def get_need_exp(self):
        return self.get_level_exp() - self.get_level()

    def get_all_exp(self):
        exp = self.get_exp()
        for lv in range(self.get_level()):
            exp += 5 * lv ** 2 + (50 * lv) + 100
        return exp

    def get_daily_cash(self):
        level = self.get_level()
        if level <= 10:
            return 100
        elif level <= 20:
            return 150
        elif level <= 30:
            return 250
        elif level <= 40:
            return 350
        elif level <= 50:
            return 450
        else:
            return 500
