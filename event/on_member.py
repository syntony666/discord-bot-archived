from discord import Member
from discord.ext import commands

from dao.config_dao import ConfigDao
from core.extension import Extension


class OnMember(Extension):
    def __init__(self, bot):
        super(OnMember, self).__init__(bot)
        self.config_dao = ConfigDao()

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        guild_id = str(member.guild.id)
        data = self.config_dao.get_data(guild_id)
        if len(data) == 0:
            return
        if data[0].join_channel != '0':
            config = data[0]
            await self.bot.get_channel(int(config.join_channel)).send(config.join_message.format(m=member.mention))

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        guild_id = str(member.guild.id)
        data = self.config_dao.get_data(guild_id)
        if len(data) == 0:
            return
        if data[0].remove_channel != '0':
            config = data[0]
            await self.bot.get_channel(int(config.remove_channel)).send(config.remove_message.format(m=member))


def setup(bot):
    bot.add_cog(OnMember(bot))