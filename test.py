import discord
from discord.ext import commands
from pymongo import MongoClient
from core.util import getDatabase
import os

db = getDatabase()

collection = db['keywords']

print('connected')


post = {"server": "438997365194489856",
    "user": "328928072239939584",
    "receive": "樂高",
    "send": "好樂高！ 樂高的奧妙之處，是可以藏於眾多玩具之中，隨手可得，還可以組裝它掩藏殺機。 就算被警察抓也告不了你，真不愧為七種刑具之首！"}
collection.insert_one(post)

print('post success')
