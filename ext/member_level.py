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

    @commands.command(aliases=['info'])
    async def get_info(self, ctx):
        member = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
        query = {'server': ctx.guild.id, 'user': member.id}
        found = self.db['member-info'].find_one(query)
        if found is not None:
            embed = discord.Embed(title=member.name, color=member.color.value)
            embed.add_field(name='等級', value=found['level'], inline=False)
            embed.add_field(name='已獲得經驗', value=found['exp'], inline=True)
            embed.add_field(name='升級所需經驗值', value=get_need_exp(found['level']) - found['exp'], inline=True)
            embed.add_field(name='已傳送對話數量', value=found['msg-count'], inline=False)
            embed.add_field(name='現金', value=found['money'], inline=False)
            await ctx.send(embed=embed)

    @commands.command(aliases=['daily'])
    async def daily_cash(self, ctx):
        query = {'server': ctx.guild.id, 'user': ctx.author.id}
        found = self.db['member-info'].find_one(query)
        if found is not None:
            if datetime.now() > found['daily-money'] + timedelta(days=1):
                self.db['member-info'].find_one_and_update(query, {
                    '$set': {'money': found['money'] + get_daily_cash(found['level']),
                             'daily-money': datetime.now()}
                })
                await ctx.send(f'這是你今天的薪資 {get_daily_cash(found["level"])}')
            else:
                await ctx.send('你今天領過了，做人不要太貪心')
        else:
            await ctx.send(f'{ctx.author.mention} 目前沒說過話')


def get_need_exp(level):
    return 5 * level ** 2 + (50 * level) + 100


def get_all_exp(level, exp):
    for lv in range(level + 1):
        exp += get_need_exp(lv)
    return exp


def get_daily_cash(level):
    if level <= 10:
        return 100
    elif level <= 20:
        return 150
    elif level <= 30:
        return 250
    elif level <= 40:
        return 350
    elif level <= 50:
        return 450
    else:
        return 500


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
        db['member-info'].find_one_and_update(query, {
            '$set': {'msg-count': member_info['msg-count'] + 1,
                     'level': level,
                     'exp': exp,
                     'send-msg-time': datetime.now()}
        })


def setup(bot):
    bot.add_cog(MemberInfo(bot))
