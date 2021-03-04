from datetime import datetime

import discord
from discord.ext import commands

from core.exception import CommandSyntaxError, DataExist
from core.extension import Extension
from dao.ban_dao import BanDAO
from dao.config_dao import ConfigDAO
from helper.parse_helper import DurationParser


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
            time = datetime.now()
            BanDAO().create_ban(m.id, time, duration, reason)
            await m.add_roles(ctx.guild.get_role(ConfigDAO().get_ban_role()))
            response = BanDAO().get_ban(_id=f'{m.id}{time.strftime("%Y%m%d%H%M%S")}')[0]
            await send_embed_msg(ctx, '已加入封鎖清單', response, discord.Color.blue())
        except CommandSyntaxError:
            await ctx.send(f'指令錯誤')
        except DataExist:
            await ctx.send(f'你已經ban過了')

    @ban.command(aliases=['l'])
    async def get_ban_list(self, ctx, member):
        response = None
        if len(ctx.message.mentions) == 0:
            response = BanDAO().get_ban()
        else:
            response = BanDAO().get_ban(member_id=ctx.message.mentions.id)
        for x in response:
            await send_embed_msg(ctx, '封鎖清單', x, discord.Color.green())


async def send_embed_msg(ctx, title, response, color):
    ban_thumbnail = discord.File(
        'src/img/ban_thumbnail.png', filename='ban_thumbnail.png')
    embed = discord.Embed(title=title, color=color)
    embed.set_thumbnail(url='attachment://ban_thumbnail.png')
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f'ID: {response["_id"]}')
    embed.add_field(name='可撥仔', value=ctx.guild.get_member(int(response['member_id'])).name, inline=False)
    embed.add_field(name='開始時間', value=response['start_time'].strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name='結束時間', value=response['end_time'].strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name='時長', value=DurationParser(response['duration']).get_str(), inline=True)
    embed.add_field(name='原因', value=response['reason'], inline=True)
    embed.add_field(name='已解除封鎖', value='是' if response['unban'] else '否', inline=False)

    await ctx.send(file=ban_thumbnail, embed=embed)


def setup(bot):
    bot.add_cog(Ban(bot))
