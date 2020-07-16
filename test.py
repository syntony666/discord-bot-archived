import discord
from discord.ext import commands
from pymongo import MongoClient
import os


client = MongoClient("mongodb+srv://admin:1gDBfQklGazHlNeo@discordbotdb-iopzr.gcp.mongodb.net/bot_db?retryWrites=true&w=majority")

print('db connected')

auth = client['bot-db']['auth']

print('connected')


post = {"token" : "NzIwMjM4NTQ0Mjg2OTA4NDI2.Xuy9zQ.YwwLbNsebuSBvNERYt1kWPMS-1k",
        "uri" : "mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq",
        "database" : "heroku_vfz6lbdq",
        "prefix" : ">"}

print(auth.find_one())