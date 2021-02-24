import discord
from discord.ext import commands

from core.database import Database


class Extension(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def cog_check(self, ctx):
        return len(Database('auth').get_data({'guild_id': str(ctx.guild.id)})) != 0
