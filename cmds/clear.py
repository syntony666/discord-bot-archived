from datetime import datetime, timedelta

from discord.ext import commands

from core.extension import Extension
from helper.parse_helper import DurationParser


class Clear(Extension):
    @commands.group()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        pass

    @clear.command(aliases=['t'])
    async def clear_by_time(self, ctx, duration):
        purge_time = datetime.now() - DurationParser(duration).get_time()
        # await ctx.channel.purge(after=purge_time, limit=10000)
        await ctx.send(f'{ctx.author.mention} 刪除 __{purge_time.strftime("%Y/%m/%d %H:%M")}__ 後的訊息')

    @clear.command(aliases=['n'])
    async def clear_by_num(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)
        await ctx.send(f'{ctx.author.mention} 刪除了 {num} 則訊息')


def setup(bot):
    bot.add_cog(Clear(bot))
