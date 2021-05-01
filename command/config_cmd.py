from discord import Client, Color, Embed
from discord.ext import commands

from service.validate_service import validate_channel
from dao.config_dao import ConfigDao
from core.extension import Extension


class Config(Extension):
    def __init__(self, bot: Client):
        super(Config, self).__init__(bot)
        self.embed_color = Color.blue()
        self.config_dao = ConfigDao()

    @commands.group(aliases=['cf'])
    async def config(self, ctx: commands.Context):
        pass

    @config.command(aliases=["join-ch"])
    async def set_join_channel(self, ctx: commands.Context, channel_id: str):
        if channel_id != '0':
            validate_channel(ctx.guild, int(channel_id))
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, join_channel=channel_id)

    @config.command(aliases=["join-msg"])
    async def set_join_message(self, ctx: commands.Context, *, message: str):
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, join_message=message)

    @config.command(aliases=["remove-ch"])
    async def set_remove_channel(self, ctx: commands.Context, channel_id: str):
        if channel_id != '0':
            validate_channel(ctx.guild, int(channel_id))
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, remove_channel=channel_id)

    @config.command(aliases=["remove-msg"])
    async def set_remove_message(self, ctx: commands.Context, *, message: str):
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        self.config_dao.update_data(ctx.guild.id, remove_message=message)

    @config.command(aliases=["l"])
    async def get_config(self, ctx: commands.Context):
        if len(self.config_dao.get_data(ctx.guild.id)) == 0:
            self.config_dao.create_data(ctx.guild.id)
        config = self.config_dao.get_data(ctx.guild.id)[0]

        join_channel = f'https://discord.com/channels/{ctx.guild.id}/{config.join_channel}' \
            if config.join_channel != '0' else "未設定"
        join_msg = config.join_message.format(m=ctx.author.mention) if config.join_channel != '0' else "未設定"
        remove_channel = f'https://discord.com/channels/{ctx.guild.id}/{config.remove_channel}' \
            if config.remove_channel != '0' else "未設定"
        remove_msg = config.remove_message.format(m=ctx.author) if config.remove_channel != '0' else "未設定"

        embed = Embed(title=ctx.guild, description="這是工具人在貴伺服器的設定列表")
        embed.set_author(name=ctx.guild.owner, icon_url=ctx.guild.owner.avatar_url)
        embed.add_field(
            name="新成員歡迎訊息",
            value=f"頻道:\n{join_channel}\n"
                  f"訊息:\n{join_msg}",
            inline=False
        )
        embed.add_field(
            name="成員離開訊息",
            value=f"頻道:\n{remove_channel}\n"
                  f"訊息:\n{remove_msg}",
            inline=False
        )

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Config(bot))
