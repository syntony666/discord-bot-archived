import discord
from discord.ext import commands
from pymongo import MongoClient
from core.extension import Extension

class Reply(Extension):

    @commands.group()
    async def reply(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send('指令說明：\n>reply a [聽到的話] [要回答的話]\n>reply d [要刪掉的話]')

    @reply.command()
    async def a(self, ctx, keyword, *,msg):
        server = str(ctx.message.guild.id)
        found = self.db['keywords'].find_one({'server' : server, 'receive': keyword})
        await ctx.channel.purge(limit = 1)
        if found is not None:
            self.db['keywords'].find_one_and_update({'server' : server, 'receive': keyword},{'$set':{'send': msg}})
            await ctx.send(f'{ctx.author.mention} 教我把 **{keyword}** 的回答改成 **{msg}**')
            return
        self.db['keywords'].insert({'server' : server,'user': ctx.author.id, 'receive': keyword, 'send': msg})
        await ctx.send(f'{ctx.author.mention} 教我聽到人家說 **{keyword}** 要回答 **{msg}**')

    @reply.command()
    async def d(self, ctx, keyword):
        server = str(ctx.message.guild.id)
        found = self.db['keywords'].find_one({'server' : server, 'receive': keyword})
        await ctx.channel.purge(limit = 1)
        if found is not None:
            self.db['keywords'].find_one_and_delete({'server' : server, 'receive': keyword})
            await ctx.send(f'{ctx.author.mention} 當你說 **{keyword}** 時候 我不會理你')
            return
        await ctx.send(f'{ctx.author.mention} 沒人叫我聽到 **{keyword}** 的時候要回答')

def setup(bot):
    bot.add_cog(Reply(bot))