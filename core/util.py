import discord
from discord.ext import commands
from pymongo import MongoClient
import os


def getDatabase():
    # get variable from heroku var
    username = os.environ.get('MONGODB_USERNAME')
    password = os.environ.get('MONGODB_PASSWORD')
    dbname = 'bot-db'
    # access data from MongoDB
    db = MongoClient(
        f'mongodb+srv://{username}:{password}@discordbotdb-iopzr.gcp.mongodb.net/{dbname}?retryWrites=true&w=majority')
    return db[dbname]


def setEmbedList(title: str, description: str, context: dict):
    embed = discord.Embed(title=title, description=description, color=0xff2600)
    for name, value in context.items():
        embed.add_field(name=name, value=value, inline=False)
    return embed


def invokedNoSubcommand(ctx: discord.ext.commands.context):
    if ctx.invoked_subcommand is None:
        raise commands.MissingRequiredArgument


def isChannelInGuild(channelId: int, guild: discord.Guild):
    for channel in guild.channels:
        if channel.id == channelId:
            return True
    return False


def isRoleInGuild(roleId: int, guild: discord.Guild):
    for role in guild.roles:
        if role.id == roleId:
            return True
    return False


async def getChannelByMessage(messageId: int, guild: discord.Guild):
    for channel in guild.text_channels:
        try:
            await channel.fetch_message(messageId)
            return channel
        except discord.NotFound:
            pass
    return None
