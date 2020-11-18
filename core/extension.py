from discord.ext import commands
from core.util import get_database


class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = get_database()
