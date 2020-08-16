import discord
from discord.ext import commands
from core.extension import Extension
import datetime
import asyncio

class Poll(Extension):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reactions = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')
        self.cooldown = 0

        async def poll_task():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                if self.cooldown == 0:
                    await asyncio.sleep(1)
                    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
                    poll = self.db['poll'].find_one({'time' : now_time})
                    if poll is not None:
                        channel = self.bot.get_channel(int(poll['channel']))
                        msg = await self.bot.get_channel(int(poll['message']['channel'])).fetch_message(int(poll['message']['message']))
                        embed = discord.Embed(title = poll['question'], color = 3553599)
                        
                        for x, reaction in enumerate(msg.reactions):
                            if(reaction.emoji != self.reactions[x]):
                                await channel.send('有人亂來，沒辦法計票！！！！')
                                self.db['poll'].find_one_and_delete({'time' : now_time})
                                break
                            embed.add_field(name = poll['options'][x], value=str(reaction.count-1),inline=False)
                        self.db['poll'].find_one_and_delete({'time' : now_time})
                        await channel.send(embed=embed)
                        self.cooldown = 1
                elif self.cooldown == 1:
                    await asyncio.sleep(1)
                    self.cooldown = 0

        self.time_task = self.bot.loop.create_task(poll_task())
    
    @commands.group()
    @commands.is_owner()
    async def poll(self, ctx):
        pass
    
    @poll.command()
    async def a(self, ctx, question, *options: str):
        # await ctx.channel.purge(limit = 1)
        if len(options)>10:
            await ctx.send('你只能給10個選項')
            return

        server = str(ctx.message.guild.id)
        channel = str(ctx.message.channel.id)
        description = list()

        for x, option in enumerate(options):
            description += '\n\n{} {}'.format(self.reactions[x], option)
        embed = discord.Embed(title = question, color = 3553599, description = ''.join(description))
        embed.set_footer(text='發起者: {}'.format(ctx.author.name))
        react_message = await ctx.send(embed = embed)

        for x, option in enumerate(options):
            await react_message.add_reaction(self.reactions[x])

        self.db['poll'].insert({'server' : server, 'channel': channel, 'time':'202008110028', 'message': {'channel':channel,'message':str(react_message.id)}, 'question':question, 'options': list(options)})
def setup(bot):
    bot.add_cog(Poll(bot))