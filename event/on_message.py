from discord.ext import commands

from core.extension import Extension
from dao.reply_dao import ReplyDao


class OnMessage(Extension):
    def __init__(self, bot):
        super(OnMessage, self).__init__(bot)
        self.col_name = 'reply'
        self.reply_dao = ReplyDao()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            await self.reply_message(message)

    async def reply_message(self, message):
        found = self.reply_dao.get_data(str(message.guild.id), message.content)
        if len(found) != 0:
            await message.channel.send(
                found[0].send.format(m=message.author.mention))


def setup(bot):
    bot.add_cog(OnMessage(bot))
