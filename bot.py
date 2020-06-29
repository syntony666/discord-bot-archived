import discord
from discord.ext import commands
from pymongo import MongoClient
import os

ext_path = 'bots'
db = MongoClient('mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq').heroku_vfz6lbdq
auth = db['auth'].find_one()
bot = commands.Bot(command_prefix=auth['prefix'])

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

    bot.run(auth['token'])