from datetime import datetime

import discord
from discord.ext import commands

from core.exception import CommandSyntaxError, DataExist
from core.extension import Extension
from dao.ban_dao import BanDAO
from dao.config_dao import ConfigDAO


class Ban(Extension):
    @commands.has_permissions(manage_messages=True)
    @commands.group()
    async def ban(self, ctx):
        pass

    @ban.command(aliases=['a'])
    async def add_ban(self, ctx, member, duration, *, reason):
        try:
            if len(ctx.message.mentions) == 0:
                raise CommandSyntaxError
            m = ctx.message.mentions[0]
            BanDAO().create_ban(m.id, datetime.now(), duration, reason)
            await m.add_roles(ctx.guild.get_role(ConfigDAO().get_ban_role()))
            embed = discord.Embed(title='__已新增封鎖清單__', color=0x3ea076)
            embed.add_field(name='可撥仔', value=m.name, inline=False)
            embed.add_field(name='封鎖時長', value=duration, inline=False)
            embed.add_field(name='原因', value=reason, inline=False)
            await ctx.send(embed=embed)
        except CommandSyntaxError:
            await ctx.send(f'指令錯誤')
        except DataExist:
            await ctx.send(f'你已經ban過了')
    @commands.has_permissions(manage_messages=True)
    @commands.group()
    async def ban(self, ctx):
        pass

    @ban.command(aliases=['a'])
    async def add_ban(self, ctx, member, duration, *, reason):
        try:
            if len(ctx.message.mentions) == 0:
                raise CommandSyntaxError
            m = ctx.message.mentions[0]
            BanDAO().create_ban(m.id, datetime.now(), duration, reason)
            await m.add_roles(ctx.guild.get_role(ConfigDAO().get_ban_role()))
            embed = discord.Embed(title='__已新增封鎖清單__', color=0x3ea076)
            embed.add_field(name='可撥仔', value=m.name, inline=False)
            embed.add_field(name='封鎖時長', value=duration, inline=False)
            embed.add_field(name='原因', value=reason, inline=False)
            await ctx.send(embed=embed)
        except CommandSyntaxError:
            await ctx.send(f'指令錯誤')
        except DataExist:
            await ctx.send(f'你已經ban過了')

    @ban.command(aliases=['l'])
    async def get_ban_list(self, ctx):
        try:
            if len(ctx.message.mentions) == 0:
                raise CommandSyntaxError
            BanDAO().get_ban()
            embed = discord.Embed(title='__已新增封鎖清單__', color=0x3ea076)

        except CommandSyntaxError:
            await ctx.send(f'指令錯誤')

    @ban.command(aliases=['l'])
    async def get_ban_list(self, ctx):
        try:
            if len(ctx.message.mentions) == 0:
                raise CommandSyntaxError
            BanDAO().get_ban()
            embed = discord.Embed(title='__已新增封鎖清單__', color=0x3ea076)

        except CommandSyntaxError:
            await ctx.send(f'指令錯誤')


def setup(bot):
    bot.add_cog(Ban(bot))
