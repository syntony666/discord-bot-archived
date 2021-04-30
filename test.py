import json

from pymongo import MongoClient

from config_dao import ConfigDao
from database import Database
from setting import DATABASE_NAME, DATABASE_URL

data = [
    {
        "_id": {
            "guild": "765871580768501790"
        },
        "join_channel": "766277899023024178",
        "join_message": "{m} 跑進來了 不知道會不會按電鈴",
        'remove_channel': '766277899023024178',
        'remove_message': '{m} 再見 後會有期'
    }
]
MongoClient(DATABASE_URL).get_database(DATABASE_NAME).get_collection('config').insert_many(data)
