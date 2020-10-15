import discord
from discord.ext import commands

from core.extension import Extension


class ReactionRole(Extension):
    @commands.group(aliases=['rr'])
    @commands.has_permissions(administrator=True)
    async def reaction_role(self, ctx):
        self.invokedNoSubcommand(ctx)

    @reaction_role.command(aliases=['a'])
    async def add_reaction_role(self, ctx, message_id: int, emoji: discord.Emoji, role_id: int):
        self.db['role-setting'].insert_one({
            'server': ctx.guild.id,
            'message_id': message_id,
            'emoji': str(emoji),
            'role': role_id
        })


def setup(bot):
    bot.add_cog(ReactionRole(bot))
