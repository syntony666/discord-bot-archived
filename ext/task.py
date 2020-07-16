import discord
from discord.ext import commands
# from pymongo import MongoClient
from core.extension import Extension
# import datetime
# import asyncio

# db = MongoClient('mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq?retryWrites=false').heroku_vfz6lbdq
# team = db['team']
# teamInfo = db['team_info']

class Task(Extension):
    
    def __init__(self, *args, **kwargs):
        pass
#         super().__init__(*args, **kwargs)

#         async def time_task():
#             await self.bot.wait_until_ready()
#             while not self.bot.is_closed():
#                 await asyncio.sleep(20)
#         self.time_task = self.bot.loop.create_task(time_task())

#     @commands.group()
#     async def team(self, ctx):
#         # usage
#         pass

#     # @commands.has_permissions(manage_messages=True)
#     @team.command()
#     async def setPost(self, ctx, channel:int):
#         server = str(ctx.message.guild.id)
#         found = teamInfo.find_one({'server' : server})
#         await ctx.channel.purge(limit = 1)
#         if found is not None:
#             teamInfo.find_one_and_update({'server' : server},{'$set':{'channel': channel}})
#             await ctx.send(f'{ctx.author.mention} 隊伍資訊已經改到 <#{str(channel)}>')
#             return
#         teamInfo.insert({'server' : server, 'channel': channel})
#         await ctx.send(f'{ctx.author.mention} 隊伍資訊公告 <#{str(channel)}>')

#     @team.command()
#     async def create(self, ctx, instance, num, time, own, req, channel, *, memo):
#         await ctx.send('created')
#         server = str(ctx.message.guild.id)
#         embed=discord.Embed(title=f'{instance} {num}場', description=time, color=0xff2600)
#         embed.add_field(name="要求配置", value= req, inline=False)
#         embed.add_field(name="名字", value= f'{ctx.author.mention}', inline=True)
#         embed.add_field(name="配置", value=own, inline=True)
#         embed.add_field(name="隊伍頻道", value= f'<#{channel}>', inline=False)
#         embed.add_field(name="備註", value= memo, inline=False)
#         mes_id = await ctx.send(embed=embed)
#         team.insert({'server': server,'message': mes_id, 'player': [ctx.author.id], 'instance': instance,
#                      'num': num, 'time': time, 'own': own, 'req': req, 'channel':channel, 'memo': memo})

def setup(bot):
    bot.add_cog(Task(bot))