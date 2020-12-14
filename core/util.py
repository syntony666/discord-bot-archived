import discord
from discord.ext import commands
from pymongo import MongoClient
import os


def get_database():
    # get variable from heroku var
    username = os.environ.get('MONGODB_USERNAME')
    password = os.environ.get('MONGODB_PASSWORD')
    dbname = 'bot-db'
    # access data from MongoDB
    db = MongoClient(
        f'mongodb+srv://{username}:{password}@discordbotdb.iopzr.mongodb.net/{dbname}?retryWrites=true&w=majority')
    return db[dbname]


def set_embed_list(title: str, description: str, context: dict):
    embed = discord.Embed(title=title, description=description, color=0xff2600)
    for name, value in context.items():
        embed.add_field(name=name, value=value, inline=False)
    return embed


def invoked_no_subcommand(ctx: discord.ext.commands.context):
    if ctx.invoked_subcommand is None:
        raise commands.MissingRequiredArgument


def is_channel_in_guild(channel_id: int, guild: discord.Guild):
    for channel in guild.channels:
        if channel.id == channel_id:
            return True
    return False


def is_role_in_guild(role_id: int, guild: discord.Guild):
    for role in guild.roles:
        if role.id == role_id:
            return True
    return False


async def get_channel_by_message(message_id: int, guild: discord.Guild):
    for channel in guild.text_channels:
        try:
            await channel.fetch_message(message_id)
            return channel
        except discord.NotFound:
            pass
    return None


def get_all_command(bot):
    command_list = list()
    for command in bot.commands:
        command_list.append(command.name)
        for alias in command.aliases:
            command_list.append(alias)
    return command_list


def get_member_rank(guild: int, filters: list):
    return list(get_database().get_collection('member-info').find({'server': guild}).sort(filters))
