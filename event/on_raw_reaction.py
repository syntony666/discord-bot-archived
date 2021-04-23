from discord.ext import commands

from core.extension import Extension
from dao.reaction_role_dao import ReactionRoleDao


class OnRawReaction(Extension):
    def __init__(self, bot):
        super(OnRawReaction, self).__init__(bot)
        self.col_name = 'reaction_role'
        self.reaction_role_dao = ReactionRoleDao()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = str(payload.guild_id)
        message_id = str(payload.message_id)
        emoji = str(payload.emoji)
        reaction_role = self.reaction_role_dao.get_data(guild_id, message=message_id, emoji=emoji)
        if len(reaction_role) != 0:
            await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(int(reaction_role[0].role)))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        guild_id = str(payload.guild_id)
        message_id = str(payload.message_id)
        emoji = str(payload.emoji)
        reaction_role = self.reaction_role_dao.get_data(guild_id, message=message_id, emoji=emoji)
        if len(reaction_role) != 0:
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(int(reaction_role[0].role)))


def setup(bot):
    bot.add_cog(OnRawReaction(bot))