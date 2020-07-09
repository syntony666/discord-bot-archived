import discord
from discord.ext import commands
from core.bot_db import MongoDB as mongo
import os

# from exceptions import Exceptions

ext_path = 'ext'
db = mongo()
bot = commands.Bot(command_prefix=db.auth('prefix'))

for file in os.listdir('./'+ ext_path):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f'{ext_path}.{name}')

if __name__ == "__main__":
    bot.run(db.auth('token'))