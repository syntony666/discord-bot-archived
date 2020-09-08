import asyncio
import datetime

from datetime import datetime, timedelta

from discord.ext import commands

from core.extension import Extension


class Reminder(Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def reminder_no_repeat():
            await self.bot.wait_until_ready()
            now_time = ''
            while not self.bot.is_closed():
                await asyncio.sleep(1)
                if now_time == datetime.now().strftime('%Y%m%d%H%M'):
                    continue
                now_time = datetime.now().strftime('%Y%m%d%H%M')
                query = {"repeat": "none", "time": now_time}
                if self.db['reminder'].find_one(query) is not None:
                    for reminds in self.db['reminder'].find(query):
                        await self.bot.get_channel(reminds['channel']).send(reminds['message'])
                    self.db['reminder'].delete_many(query)

        async def reminder_repeat_everyday():
            await self.bot.wait_until_ready()
            now_time = ''
            while not self.bot.is_closed():
                await asyncio.sleep(1)
                if now_time == datetime.now().strftime('%H%M'):
                    continue
                now_time = datetime.now().strftime('%H%M')
                query = {"repeat": "day", "time": now_time}
                if self.db['reminder'].find_one(query) is not None:
                    for reminds in self.db['reminder'].find(query):
                        await self.bot.get_channel(reminds['channel']).send(reminds['message'])

        async def reminder_repeat_every_month():
            await self.bot.wait_until_ready()
            now_time = ''
            while not self.bot.is_closed():
                await asyncio.sleep(1)
                if now_time == datetime.now().strftime('%d%H%M'):
                    continue
                now_time = datetime.now().strftime('%d%H%M')
                query = {"repeat": "month", "time": now_time}
                if self.db['reminder'].find_one(query) is not None:
                    for reminds in self.db['reminder'].find(query):
                        await self.bot.get_channel(reminds['channel']).send(reminds['message'])

        self.reminder_no_repeat = self.bot.loop.create_task(reminder_no_repeat())
        self.reminder_repeat_everyday = self.bot.loop.create_task(reminder_repeat_everyday())
        self.reminder_repeat_every_month = self.bot.loop.create_task(reminder_repeat_every_month())

    @commands.group()
    async def reminder(self, ctx):
        self.invokedNoSubcommand(ctx)

    @reminder.command(aliases=['rd', 'day'])
    async def repeat_by_day(self, ctx: commands.Context, hour: int, minute: int, title, *, msg):
        if self.db['reminder'].find_one({"server": ctx.guild.id, "title": title}) is not None:
            await ctx.send(f'標題名稱相同，無法建立提醒')
            return
        setTime = datetime(2020, 1, 1, hour=hour, minute=minute)
        self.db['reminder'].insert_one({
            "server": ctx.guild.id,
            "channel": ctx.channel.id,
            "repeat": "day",
            "time": setTime.strftime('%H%M'),
            "title": title,
            "message": msg
        })
        embed = {
            "title": title,
            "description": '',
            "context": {
                "時間": setTime.strftime("每天 %H:%M"),
                "訊息": msg
            }
        }
        await ctx.send(f'{ctx.author.mention} 建立了一個提醒',
                       embed=self.setEmbedList(embed["title"], embed["description"], embed["context"]))

    @reminder.command(aliases=['rm', 'month'])
    async def repeat_by_month(self, ctx, day: int, hour: int, minute: int, title, *, msg):
        if self.db['reminder'].find_one({"server": ctx.guild.id, "title": title}) is not None:
            await ctx.send(f'標題名稱相同，無法建立提醒')
            return
        setTime = datetime(2020, 1, day, hour=hour, minute=minute)
        self.db['reminder'].insert_one({
            "server": ctx.guild.id,
            "channel": ctx.channel.id,
            "repeat": "month",
            "time": setTime.strftime('%d%H%M'),
            "title": title,
            "message": msg
        })
        embed = {
            "title": title,
            "description": '',
            "context": {
                "時間": setTime.strftime("每個月%d號 %H:%M"),
                "訊息": msg
            }
        }
        await ctx.send(f'{ctx.author.mention} 建立了一個提醒',
                       embed=self.setEmbedList(embed["title"], embed["description"], embed["context"]))

    @reminder.command(aliases=['o', 'once'])
    async def just_remind_once(self, ctx, year: int, month: int, day: int, hour: int, minute: int, *, msg):
        setTime = datetime(year, month, day, hour=hour, minute=minute, second=0)
        if datetime.now() > setTime:
            await ctx.send('時間不會回溯')
            return
        if datetime.now() + timedelta(days=30) < setTime:
            await ctx.send('不接受30天後的提醒')
        self.db['reminder'].insert_one({
            "server": ctx.guild.id,
            "channel": ctx.channel.id,
            "repeat": "none",
            "time": setTime.strftime('%Y%m%d%H%M'),
            "message": msg
        })
        embed = {
            "title": '提醒',
            "description": '',
            "context": {
                "時間": setTime.strftime("%Y/%m/%d %H:%M"),
                "訊息": msg
            }
        }
        await ctx.send(f'{ctx.author.mention} 建立了一個提醒',
                       embed=self.setEmbedList(embed["title"], embed["description"], embed["context"]))

    @reminder.command(alias=['d', 'delete'])
    async def delete_reminders(self, ctx, title):
        query = {'server': ctx.guild.id, "title": title}
        self.db['reminder'].delete_many(query)


def setup(bot):
    bot.add_cog(Reminder(bot))
