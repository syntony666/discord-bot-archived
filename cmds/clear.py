from datetime import datetime, timedelta

import discord
from discord.ext import commands

from core.extension import Extension
from helper.parse_helper import DurationParser


class Clear(Extension):
    @commands.group()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        pass

    @clear.command(aliases=['time'])
    async def clear_by_time(self, ctx, year: int, month: int, day: int, hour: int = 0, minute: int = 0):
        purge_time = datetime(year, month, day, hour=hour, minute=minute)
        await ctx.channel.purge(after=purge_time - timedelta(hours=8), limit=10000)
        await send_embed_msg(ctx, f'刪除了 **{purge_time.strftime("%Y/%m/%d %H:%M")}** 後的訊息')

    @clear.command(aliases=['dur'])
    async def clear_by_time(self, ctx, duration):
        purge_time = datetime.now() - DurationParser(duration).get_time()
        await ctx.channel.purge(after=purge_time - timedelta(hours=8), limit=1000)
        await send_embed_msg(ctx, f'刪除了 **{purge_time.strftime("%Y/%m/%d %H:%M")}** 後的訊息')

    @clear.command(aliases=['num'])
    async def clear_by_num(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)
        await send_embed_msg(ctx, f'刪除了 **{num}** 則訊息')


async def send_embed_msg(ctx, description):
    embed = discord.Embed(title='已刪除訊息', color=discord.Color.gold(), description=description)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Clear(bot))
