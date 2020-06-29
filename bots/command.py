import discord
from discord.ext import commands
from pymongo import MongoClient
from extension import Extension

db = MongoClient('mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq').heroku_vfz6lbdq
keywords = db['keywords']

class Command(Extension):
    @commands.command()
    async def status(self, ctx):
        await ctx.send(f'{self.bot.latancy*1000}')
    
    @commands.command()
    async def list(self, ctx):
        msg = '```\n'
        for x in keywords.find({"server" : str(ctx.message.guild.id)},{'_id' : 0, 'receive' : 1, 'send' : 1}):
            msg+=str(x)+'\n'
        await ctx.send(f'{msg}```')
    
    @commands.command()
    @commands.has_permissions(manage_messages==True)
    async def clear(self, ctx, num:int):
        await ctx.channel.purge(limit = num+1)
        await ctx.send(f'<@{ctx.author.id}> 刪除了 {num} 則訊息')


    @commands.command()
    async def teach(self, ctx, keyword, *,msg):
        await ctx.send(keyword)
         

def setup(bot):
    bot.add_cog(Command(bot))