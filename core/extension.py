from discord.ext import commands
from core.util import getDatabase


class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = getDatabase()
