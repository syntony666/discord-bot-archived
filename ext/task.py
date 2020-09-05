import discord
from discord.ext import commands
from core.extension import Extension
import datetime
import asyncio


class Task(Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # async def interval():
        #     await self.bot.wait_until_ready()
        #     self.channel = self.bot.get_channel(610800968757542913)
        #     while not self.bot.is_closed():
        #         await self.channel.send('<@552819077761073153> 我是誰？')
        #         await asyncio.sleep(20)
        # self.time_task = self.bot.loop.create_task(interval())

        # async def time_task():
        #     await self.bot.wait_until_ready()
        #     self.channel = self.bot.get_channel(727373570564423720)
        #     while not self.bot.is_closed():
        #         now_time = datetime.datetime.now().strftime('%H%M')
        #         if now_time == "2318":
        #             await self.channel.send('<@552819077761073153> 我是誰？')
        #             await asyncio.sleep(1)
        # self.time_task = self.bot.loop.create_task(time_task())


def setup(bot):
    bot.add_cog(Task(bot))
