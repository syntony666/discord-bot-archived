import os

import discord
import psutil
from discord.ext import commands

from core.extension import Extension


class Status(Extension):
    @commands.command()
    async def about(self, ctx):
        bot_info = await self.bot.application_info()
        process = psutil.Process(os.getpid()).memory_info().rss
        percent = psutil.virtual_memory().percent
        embed = discord.Embed(title=self.bot.user.name, description=bot_info.description)
        embed.set_author(name=bot_info.owner, icon_url=bot_info.owner.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Ping', value=f'{round(self.bot.latency * 1000)} ms', inline=True)
        embed.add_field(name='Ram Usage', value=f"{round(process / 1000000)} MB ({percent}%)", inline=True)
        embed.set_footer(text="ver. 1.0.0 release")
        await ctx.send(embed=embed)

    @commands.command()
    async def stat(self, ctx):
        online_member, dnd_member, idle_member = 0, 0, 0
        vtuber, staff = 0, 0
        vtuber_id, staff_id = 785901109071839244, 811516908867551282
        for member in ctx.guild.members:
            online_member = online_member + 1 if str(member.status) != 'offline' else online_member
            dnd_member = dnd_member + 1 if str(member.status) == 'dnd' else dnd_member
            idle_member = idle_member + 1 if str(member.status) == 'idle' else idle_member
            vtuber = vtuber + 1 if vtuber_id in [x.id for x in member.roles] else vtuber
            staff = staff + 1 if staff_id in [x.id for x in member.roles] else staff
        embed = discord.Embed(title=ctx.guild.name, description=ctx.guild.description)
        embed.set_author(name=ctx.guild.owner, icon_url=ctx.guild.owner.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='創立時間', value=ctx.guild.created_at.strftime("%Y-%m-%d"), inline=False)
        embed.add_field(name='人數', value=ctx.guild.member_count, inline=False)
        embed.add_field(name='線上', value=online_member, inline=True)
        embed.add_field(name='閒置', value=idle_member, inline=True)
        embed.add_field(name='勿擾', value=dnd_member, inline=True)
        embed.add_field(name='乾爹', value=str(len(ctx.guild.premium_subscribers)), inline=False)
        embed.add_field(name='Vtuber', value=vtuber, inline=True)
        embed.add_field(name='Vtuber工作人員', value=staff, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))