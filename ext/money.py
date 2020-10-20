from datetime import timedelta, datetime

import discord
from discord.ext import commands

from core.extension import Extension
from ext.member_info import get_daily_cash


class Money(Extension):

    @commands.command()
    async def dice(self, ctx):
        pass
        

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

    @commands.command(aliases=['cash'])
    async def get_cash_command(self, ctx):
        try:
            await ctx.send(f'你現在有現金 {self.get_cash(ctx.guild.id, ctx.author.id)} 元')
        except discord.errors.InvalidData:
            await ctx.send(f'{ctx.author.mention} 目前沒說過話')

    async def set_money(self, guild_id, user_id, money):
        query = {'server': guild_id, 'user': user_id}
        found = self.db['member-info'].find_one(query)
        if found is not None:
            self.db['member-info'].find_one_and_update(query, {
                '$set': {'money': money}
            })
            return
        return discord.errors.InvalidData('Data Not Found!')

    async def get_cash(self, guild_id, user_id):
        query = {'server': guild_id, 'user': user_id}
        found = self.db['member-info'].find_one(query)
        if found is not None:
            return found['money']
        return discord.errors.InvalidData('Data Not Found!')


def setup(bot):
    bot.add_cog(Money(bot))
