import discord
from discord.ext import commands
from pymongo import MongoClient
from core.extension import Extension

class Command(Extension):
    @commands.command()
    async def status(self, ctx):
        embed=discord.Embed(title="樂高", description="不要踩會痛", color=0xff2600)
        embed.add_field(name="ping", value= str(round(self.bot.latency*1000))+' ms', inline=False)
        embed.add_field(name="狀態", value="上線中", inline=False)
        await ctx.send(embed=embed)
     
    @commands.command()
    async def list(self, ctx):
        msg = '```\n'
        for x in self.db['keywords'].find({"server" : str(ctx.message.guild.id)},{'_id' : 0, 'receive' : 1, 'send' : 1}):
            msg+=str(x)+'\n'
        await ctx.send(f'{msg}```')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num:int):
        await ctx.channel.purge(limit = num+1)
        await ctx.send(f'{ctx.author.mention} 刪除了 {num} 則訊息')


    @commands.group()
    async def teach(self, ctx):
        pass

    @teach.command()
    async def add(self, ctx, keyword, *,msg):
        server = str(ctx.message.guild.id)
        found = self.db['keywords'].find_one({'server' : server, 'receive': keyword})
        await ctx.channel.purge(limit = 1)
        if found is not None:
            self.db['keywords'].find_one_and_update({'server' : server, 'receive': keyword},{'$set':{'send': msg}})
            await ctx.send(f'{ctx.author.mention} 教我把 **{keyword}** 的回答改成 **{msg}**')
            return
        self.db['keywords'].insert({'server' : server,'user': ctx.author.id, 'receive': keyword, 'send': msg})
        await ctx.send(f'{ctx.author.mention} 教我聽到人家說 **{keyword}** 要回答 **{msg}**')

    @teach.command()
    async def delete(self, ctx, keyword):
        server = str(ctx.message.guild.id)
        found = self.db['keywords'].find_one({'server' : server, 'receive': keyword})
        await ctx.channel.purge(limit = 1)
        if found is not None:
            self.db['keywords'].find_one_and_delete({'server' : server, 'receive': keyword})
            await ctx.send(f'{ctx.author.mention} 當你說 **{keyword}** 時候 我不會理你')
            return
        await ctx.send(f'{ctx.author.mention} 沒人叫我聽到 **{keyword}** 的時候要回答')

def setup(bot):
    bot.add_cog(Command(bot))
    