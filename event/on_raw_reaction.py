from discord.ext import commands

from core.extension import Extension
from dao.reaction_role_dao import ReactionRoleDAO


class OnRawReaction(Extension):

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction_role = ReactionRoleDAO().get_rr(message_id=str(payload.message_id), emoji=str(payload.emoji))
        if reaction_role is not None and self.check_guild(payload.guild_id):
            await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(reaction_role['_id'])))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        reaction_role = ReactionRoleDAO().get_rr(message_id=str(payload.message_id), emoji=str(payload.emoji))
        if reaction_role is not None and self.check_guild(payload.guild_id):
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(int(reaction_role['_id'])))


def setup(bot):
    bot.add_cog(OnRawReaction(bot))
