from discord import Client, Color
from discord.ext import commands

from service.validate_service import validate_channel
from dao.config_dao import ConfigDao
from core.extension import Extension


class Config(Extension):
    def __init__(self, bot: Client):
        super(Config, self).__init__(bot)
        self.embed_color = Color.blue()
        self.config_dao = ConfigDao()

    @commands.group
    def config(self, ctx: commands.Context):
        pass

    @commands.command(aliases=["join-ch"])
    def set_join_channel(self, ctx: commands.Context, channel_id: str):
        validate_channel(ctx.guild, int(channel_id))
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, join_channel=channel_id)

    @commands.command(aliases=["join-msg"])
    def set_join_message(self, ctx: commands.Context, *, message: str):
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, join_message=message)

    @commands.command(aliases=["remove-ch"])
    def set_remove_channel(self, ctx: commands.Context, channel_id: str):
        validate_channel(ctx.guild, int(channel_id))
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, remove_channel=channel_id)

    @commands.command(aliases=["remove-msg"])
    def set_remove_message(self, ctx: commands.Context, *, message: str):
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, remove_message=message)


def setup(bot):
    bot.add_cog(Config(bot))
