import discord
from discord.ext import commands
from pymongo import MongoClient
import os

db = MongoClient('mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq?retryWrites=false').heroku_vfz6lbdq

post = {"token" : "NzIwMjM4NTQ0Mjg2OTA4NDI2.Xuy9zQ.YwwLbNsebuSBvNERYt1kWPMS-1k",
        "uri" : "mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq",
        "database" : "heroku_vfz6lbdq",
        "prefix" : ">"}

db['auth'].insert_one(post).inserted_id