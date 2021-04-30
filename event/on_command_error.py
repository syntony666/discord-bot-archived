from discord.ext import commands
from discord.ext.commands import ChannelNotFound, RoleNotFound, MessageNotFound

from core.extension import Extension


class OnCommandError(Extension):
    def __init__(self, bot):
        super(OnCommandError, self).__init__(bot)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, ChannelNotFound):
            await ctx.send("頻道ID輸入錯誤")
        elif isinstance(error, RoleNotFound):
            await ctx.send("身分組ID輸入錯誤")
        elif isinstance(error, MessageNotFound):
            await ctx.send("訊息ID輸入錯誤")


def setup(bot):
    bot.add_cog(OnCommandError(bot))
