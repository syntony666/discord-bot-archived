from discord import Client
from discord.ext import commands


class Extension(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
