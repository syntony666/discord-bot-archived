import discord
from discord.ext import commands
from core.extension import Extension


class Config(Extension):
    @commands.group()
    async def config(self, ctx):
        pass
    @config.command()
    async def l(self, ctx):
        pass
    async def a(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Config(bot))
