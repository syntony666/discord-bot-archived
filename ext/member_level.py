from datetime import datetime, timedelta
import random

import discord
from discord.ext import commands

from core.extension import Extension


class MemberInfo(Extension):
    @commands.command(aliases=['level'])
    async def get_level(self, ctx):
        member = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
        query = {'server': ctx.guild.id, 'user': member.id}
        found = self.db['member-info'].find_one(query)
        if found is not None:
            await ctx.send(f'{member.mention} 目前為等級 {found["level"]}')
        else:
            await ctx.send(f'{member.mention} 目前沒說過話')

    @commands.command(aliases=['exp'])
    async def get_exp(self, ctx):
        member = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
        query = {'server': ctx.guild.id, 'user': member.id}
        found = self.db['member-info'].find_one(query)
        if found is not None:
            await ctx.send(f'{member.mention} 目前說了 {found["msg-count"]} 句話\n' +
                           f'共獲得 {get_all_exp(found["level"], found["exp"])} 經驗值\n' +
                           f'再獲得 {get_need_exp(found["level"]) - found["exp"]} 經驗值就能升級')
        else:
            await ctx.send(f'{member.mention} 目前沒說過話')


def get_need_exp(level):
    return 5 * level ** 2 + (50 * level) + 100


def get_all_exp(level, exp):
    for lv in range(level + 1):
        exp += get_need_exp(lv)
    return exp


def message_exp(db, member: discord.Member):
    query = {'server': member.guild.id, 'user': member.id}
    member_info = db['member-info'].find_one(query)
    new_exp = random.randint(10, 30)
    if member_info is None:
        db['member-info'].insert_one({
            'server': member.guild.id,
            'user': member.id,
            'msg-count': 1,
            'level': 0,
            'exp': new_exp,
            'send-msg-time': datetime.now(),
            'money': 0,
            'daily-money': datetime.now()
        })
    elif datetime.now() > member_info['send-msg-time'] + timedelta(minutes=1):
        exp = member_info['exp'] + new_exp
        print(exp)
        level = member_info['level']
        if exp > get_need_exp(level):
            exp -= get_need_exp(level)
            level += 1
        db['member-info'].find_one_and_update(query, {'$set': {'msg-count': member_info['msg-count'] + 1,
                                                               'level': level,
                                                               'exp': exp,
                                                               'send-msg-time': datetime.now()}})


def setup(bot):
    bot.add_cog(MemberInfo(bot))
