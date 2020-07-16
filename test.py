import discord
from discord.ext import commands
from pymongo import MongoClient
from core.util import getDatabase
import os

db = getDatabase()

collection = db['welcome']

print('connected')


post = {    "server": "438997365194489856",
    "channel": "676414129145249792",
    "message": "歡迎加入，請問是玩什麼遊戲呢?"}
collection.insert_one(post)
