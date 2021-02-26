import random
import time
from datetime import datetime, timedelta

from discord.ext import commands

from core.extension import Extension
from dao.reply_dao import ReplyDAO


class OnMessage(Extension):

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.content)
        if message.author != self.bot.user:
            await reply_message(message)


async def reply_message(message):
    found = list(filter(lambda reply:
                        reply['_id'] == message.content, ReplyDAO().get_reply()))
    if len(found) != 0:
        await message.channel.send(found[0]['value']
                                   .format(m=message.author.mention))


def setup(bot):
    bot.add_cog(OnMessage(bot))
