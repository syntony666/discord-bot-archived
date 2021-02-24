import os

import discord
from discord.ext import commands
from core.database import Database

auth = Database('auth').get_data({"_id": "test"})[0]
dirs = ['cmds', 'event']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=auth['prefix'], help_command=None, intents=intents)


def load_extension(paths):
    for path in paths:
        for file in os.listdir('./' + path):
            if file.endswith(".py"):
                name = file[:-3]
                bot.load_extension(f'{path}.{name}')


load_extension(dirs)

if __name__ == "__main__":
    bot.run(auth['token'])
