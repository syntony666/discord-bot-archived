from discord import Client, Color, Embed
from discord.ext import commands

from core.extension import Extension
from dao.reaction_role_dao import ReactionRoleDao
from core.exception import DataExist, DataNotExist
from service.validate_service import validate_role, validate_message, get_channel_by_message


class ReactionRole(Extension):
    def __init__(self, bot: Client):
        super(ReactionRole, self).__init__(bot)
        self.embed_color = Color.blue()
        self.reaction_role_dao = ReactionRoleDao()

    @commands.has_permissions(administrator=True)
    @commands.group(aliases=['rr'])
    async def reaction_role(self, ctx):
        pass

    @reaction_role.command(aliases=['a'])
    async def set_reaction_role(self, ctx, role_id, message_id, reaction):
        try:
            guild_id = str(ctx.guild.id)
            validate_role(ctx.guild, role_id)
            await validate_message(ctx.guild, message_id)
            channel = await get_channel_by_message(ctx.guild, message_id)
            self.reaction_role_dao.create_data(guild_id, role_id, message_id, reaction)
            embed = Embed(title='已新增表情身份組', color=self.embed_color)
            embed.add_field(name='訊息網址',
                            value=f'https://discord.com/channels/{ctx.guild.id}/{channel.id}/{message_id}',
                            inline=False)
            embed.add_field(name=str(reaction), value=f'<@&{role_id}>', inline=False)
            message = await channel.fetch_message(message_id)
            await message.add_reaction(reaction)
            await ctx.send(embed=embed)
        except DataExist:
            await ctx.send(f'已設定此身份組的表情身份組')

    @reaction_role.command(aliases=['d'])
    async def del_reaction_role(self, ctx, role_id):
        try:
            guild_id = str(ctx.guild.id)
            self.reaction_role_dao.del_data(guild_id, role=role_id)
            await ctx.send(f'已刪除 <@&{role_id}> 表情身分組')
        except DataNotExist:
            await ctx.send(f'找不到此身份組的表情身份組')

    @reaction_role.command(aliases=['dm'])
    async def del_reaction_role_by_message(self, ctx, message_id):
        try:
            guild_id = str(ctx.guild.id)
            self.reaction_role_dao.del_data(guild_id, message=message_id)
            channel = await get_channel_by_message(ctx.guild, message_id)
            await ctx.send(f'已刪除在 https://discord.com/channels/{ctx.guild.id}/{channel.id}/{message_id} 設定的的表情身分組')
        except DataNotExist:
            await ctx.send(f'找不到此訊息的表情身份組')


def setup(bot):
    bot.add_cog(ReactionRole(bot))
