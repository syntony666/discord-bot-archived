import discord
from discord.ext import commands
from pymongo import MongoClient
from core.util import getDatabase
import os

mongoClient = MongoClient(f'mongodb+srv://admin:M9IHInqE44aRmAXI@discordbotdb-iopzr.gcp.mongodb.net/bot-db?retryWrites=true&w=majority')
db = mongoClient['bot-db']
collection = db['aaa']

print('connected')


post = {"foo":"bar"}
collection.insert_one(post)

print(collection.find_one())
