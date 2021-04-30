from discord.ext import commands

from core.extension import Extension


class OnGuild(Extension):
    def __init__(self, bot):
        super(OnGuild, self).__init__(bot)

    @commands.Cog.listener()
    async def on_guild_join(self):
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self):
        pass


def setup(bot):
    bot.add_cog(OnGuild(bot))
