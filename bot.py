import os

import discord
from discord.ext import commands

from core.util import getDatabase

ext_path = 'ext'
db = getDatabase()
auth = db['auth'].find_one()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=auth['prefix'], help_command=None, intents=intents)

for file in os.listdir('./' + ext_path):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f'{ext_path}.{name}')

if __name__ == "__main__":
    bot.run(auth['token'])
