from datetime import datetime, timedelta

from discord.ext import commands

from core.extension import Extension
from dao.config_dao import ConfigDAO
from impl.guild_impl import validate_role


class Config(Extension):
    @commands.group(aliases=['set'])
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        pass

    @config.command(aliases=['ban'])
    async def set_ban(self, ctx, role_id):
        validate_role(ctx.guild, role_id)
        ConfigDAO().set_ban_role(role_id)


def setup(bot):
    bot.add_cog(Config(bot))
