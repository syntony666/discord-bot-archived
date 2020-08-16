import discord
from discord.ext import commands
from core.util import getDatabase

class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = getDatabase()
    
    def setEmbedList(self, title: str, description: str, context :dict):
        embed = discord.Embed(title=title, color=0xff2600)
        for name, value in context.items():
            embed.add_field(name=name,value=value,inline=False)
        return embed
