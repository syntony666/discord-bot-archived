from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from core.extension import Extension


class Author(Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, guild, channel, *, msg):
        await self.bot.get_guild(int(guild)).get_channel(int(channel)).send(msg)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        data = {
            'title': 'aaa',
            'field': {
                'name': 'bbb',
                'value': 'ccc'
            }
        }
        embed = discord.Embed(**data)


def setup(bot):
    bot.add_cog(Author(bot))
