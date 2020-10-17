import discord
from discord.ext import commands

from core.extension import Extension


class Member(Extension):
    pass


def setup(bot):
    bot.add_cog(Member(bot))
