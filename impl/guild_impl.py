import discord
from discord import NotFound
from discord.ext.commands import ChannelNotFound, RoleNotFound, MessageNotFound


def validate_channel(guild: discord.Guild, channel_id: int):
    if int(channel_id) not in guild.text_channels:
        raise ChannelNotFound('Please type correct channel ID.')


def validate_role(guild: discord.Guild, role_id: int):
    if int(role_id) not in [x.id for x in guild.roles]:
        raise RoleNotFound('Please type correct role ID.')


def validate_member(guild: discord.Guild, member_id: int):
    if int(member_id) not in [x.id for x in guild.members]:
        raise RoleNotFound('Please type correct member ID.')


async def validate_message(guild: discord.Guild, message_id: int):
    for channel in guild.text_channels:
        try:
            await channel.fetch_message(message_id)
            return
        except discord.NotFound:
            pass
    raise MessageNotFound('Please type correct message ID.')


async def get_channel_by_message(guild: discord.Guild, message_id):
    for channel in guild.text_channels:
        try:
            await channel.fetch_message(message_id)
            return channel
        except NotFound:
            pass
    return None

