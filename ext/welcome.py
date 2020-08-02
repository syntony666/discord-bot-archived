import discord
from discord.ext import commands
from pymongo import MongoClient
from core.extension import Extension

class Welcome(Extension):

    @commands.command()
    async def welcome(self, ctx, welmes):
        server = str(ctx.message.guild.id)
        found = self.db['welcome'].find_one({'server' : server})
        await ctx.channel.purge(limit = 1)
        if found is not None:
            self.db['welcome'].find_one_and_update({'server' : server},{'$set':{'message': welmes}})
            await ctx.send(f'**{ctx.message.guild}** 的歡迎訊息為 **{welmes}**')
            return
        await ctx.send(f'**{ctx.message.guild}** 未設定歡迎訊息')


def setup(bot):
    bot.add_cog(Welcome(bot))