import discord
from discord.ext import commands
from core.util import getDatabase


class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = getDatabase()

    def setEmbedList(self, title: str, description: str, context: dict):
        embed = discord.Embed(title=title, description=description, color=0xff2600)
        for name, value in context.items():
            embed.add_field(name=name, value=value, inline=False)
        return embed

    def isChannelInGuild(self, channelId: int, server):
        for channel in server.channels:
            if channel.id == channelId:
                return True
        return False
