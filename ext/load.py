import discord
from discord.ext import commands
from pymongo import MongoClient
from core.extension import Extension

db = MongoClient('mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq').heroku_vfz6lbdq

welcome, keywords = db['welcome'], db['keywords']

class Load(Extension):
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        bot.load_extension(f'{ext_path}.{name}')
        await ctx.send(f'loaded {extension} done.')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        bot.unload_extension(f'{ext_path}.{name}')
        await ctx.send(f'unloaded {extension} done.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        bot.reload_extension(f'{ext_path}.{name}')
        await ctx.send(f'reloaded {extension} done.')

def setup(bot):
    bot.add_cog(Load(bot))