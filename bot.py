import discord
from discord.ext import commands
from pymongo import MongoClient
from core.bot_db import MongoDB as mongo
import os

# from exceptions import Exceptions

ext_path = 'bots'
db = mongo()
# auth = db['auth'].find_one()
bot = commands.Bot(command_prefix=db.auth('prefix'))

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'{ext_path}.{name}')
    await ctx.send(f'loaded {extension} done.')

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'{ext_path}.{name}')
    await ctx.send(f'unloaded {extension} done.')

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f'{ext_path}.{name}')
    await ctx.send(f'reloaded {extension} done.')

for file in os.listdir('./'+ext_path):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f'{ext_path}.{name}')

if __name__ == "__main__":
    print(db.auth('token'))
    bot.run(db.auth('token'))