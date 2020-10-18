import discord
from discord.ext import commands

from core.extension import Extension
from core.util import invokedNoSubcommand, getChannelByMessage, isRoleInGuild


class ReactionRole(Extension):
    @commands.group(aliases=['rr'])
    @commands.has_permissions(administrator=True)
    async def reaction_role(self, ctx):
        invokedNoSubcommand(ctx)

    @reaction_role.command(aliases=['a'])
    async def add_reaction_role(self, ctx, message_id: int, emoji: discord.Emoji, role_id: int):
        if not isRoleInGuild(role_id, ctx.guild):
            await ctx.send('not found')
            return
        channel = await getChannelByMessage(message_id, ctx.guild)
        if channel is not None:
            self.db['role-setting'].insert_one({
                'server': ctx.guild.id,
                'message_id': message_id,
                'emoji': str(emoji),
                'role': role_id
            })
            message = await channel.fetch_message(message_id)
            await message.add_reaction(emoji)
            return
        else:
            return 

    @reaction_role.command(alias=['d'])
    async def delete_one_reaction_role(self, ctx, message_id, emoji: discord.Emoji):
        self.db['role-setting'].find_one_and_delete({
            'server': ctx.guild.id,
            'message_id': message_id,
            'emoji': str(emoji)
        })

    @reaction_role.command(alias=['dm'])
    async def delete_reaction_role_by_message(self, ctx, message_id):
        if getChannelByMessage(message_id, ctx.guild) is not None:
            self.db['role-setting'].delete_many({
                'server': ctx.guild.id,
                'message_id': message_id
            })


def setup(bot):
    bot.add_cog(ReactionRole(bot))
