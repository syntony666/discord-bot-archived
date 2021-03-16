import discord
from discord.ext import commands

from core.database import Database


class Extension(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    def check_guild(self, guild: int):
        return len(Database('auth').get_data({'guild_id': str(guild)})) != 0

    async def cog_check(self, ctx):
        return self.check_guild(ctx.guild.id)
