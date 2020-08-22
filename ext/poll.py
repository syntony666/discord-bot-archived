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
        self.color = 0xffff00
        self.polls = self.db['poll']

        async def poll_task():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                if self.cooldown == 0:
                    await asyncio.sleep(1)
                    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
                    poll = self.polls.find_one({'time' : now_time})
                    if poll is not None:
                        channel = self.bot.get_channel(int(poll['channel']))
                        msg = await self.bot.get_channel(int(poll['message']['channel'])).fetch_message(int(poll['message']['messageId']))
                        embed = discord.Embed(title = poll['question'], color = self.color)
                        
                        for x, reaction in enumerate(msg.reactions):
                            if reaction.emoji != self.reactions[x]:
                                await channel.send('有人亂按，沒辦法計票！！！！')
                                break
                            embed.add_field(name = poll['options'][x], value=f'{reaction.count-1} 票',inline=False)
                        self.polls.find_one_and_delete({'time' : now_time})
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
        if len(options)>10:
            await ctx.send('你只能給10個選項')
            return

        server = ctx.message.guild.id
        channel = ctx.message.channel.id

        description = [f'\n\n{self.reactions[x]} {option}' for x, option in enumerate(options)]

        embed = discord.Embed(title = question, color = self.color, description = ''.join(description))
        embed.set_footer(text='發起者: {}'.format(ctx.author.name))
        react_message = await ctx.send(embed = embed)

        for x in range(len(options)):
            await react_message.add_reaction(self.reactions[x])

        self.polls.insert({'server' : server, 'channel': channel, 'time':'', 
                            'message': {'channel':channel,'messageId':react_message.id}, 
                            'question':question, 'options': list(options)})
        
def setup(bot):
    bot.add_cog(Poll(bot))