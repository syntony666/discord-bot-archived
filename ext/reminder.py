import asyncio
import datetime
from datetime import datetime, timedelta

from discord.ext import commands

from core.extension import Extension
from core.util import setEmbedList, invokedNoSubcommand


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

        async def reminder_repeat_task(repeat, timeFormat):
            await self.bot.wait_until_ready()
            now_time = ''
            while not self.bot.is_closed():
                await asyncio.sleep(1)
                if now_time == datetime.now().strftime(timeFormat):
                    continue
                now_time = datetime.now().strftime(timeFormat)
                query = {"repeat": repeat, "time": now_time}
                if self.db['reminder'].find_one(query) is not None:
                    for reminds in self.db['reminder'].find(query):
                        await self.bot.get_channel(reminds['channel']).send(reminds['message'])

        self.reminder_no_repeat = self.bot.loop.create_task(reminder_no_repeat())
        self.reminder_repeat_everyday = self.bot.loop.create_task(reminder_repeat_task('day', '%H%M'))
        self.reminder_repeat_every_month = self.bot.loop.create_task(reminder_repeat_task('month', '%d%H%M'))

    @commands.group()
    async def reminder(self, ctx):
        invokedNoSubcommand(ctx)

    @reminder.command(aliases=['l', 'list'])
    async def get_list(self, ctx):
        await ctx.channel.purge(limit=1)
        if self.db['reminder'].find_one({"server": ctx.guild.id}) is None:
            await ctx.send('**沒有提醒列表**')
            return
        await ctx.send('提醒列表: ')

        async def send_reminder(title, dbFormat, displayFormat):
            embed = {
                "title": title,
                "description": f'<#{reminder["channel"]}>',
                "context": {
                    "時間": datetime.strptime(reminder['time'], dbFormat).strftime(displayFormat),
                    "訊息": reminder['message']
                }
            }
            await ctx.send(embed=setEmbedList(embed["title"], embed["description"], embed["context"]))

        for reminder in self.db['reminder'].find({'server': ctx.guild.id}):
            if reminder['repeat'] == 'none':
                await send_reminder('提醒', '%Y%m%d%H%M', '%Y/%m/%d %H:%M')
            elif reminder['repeat'] == 'day':
                await send_reminder(reminder['title'], '%H%M', '每天 %H:%M')
            elif reminder['repeat'] == 'month':
                await send_reminder(reminder['title'], '%d%H%M', '每個月%d號 %H:%M')

    @reminder.command(aliases=['rd', 'day'])
    async def repeat_by_day(self, ctx, hour: int, minute: int, title, *, msg):
        await ctx.channel.purge(limit=1)
        if self.db['reminder'].find_one({"server": ctx.guild.id, "title": title}) is not None:
            await ctx.send(f'標題名稱相同，無法建立提醒')
            return
        setTime = datetime(2020, 1, 1, hour=hour, minute=minute)
        await self.send_result(ctx, 'day', setTime, '%H%M', '每天 %H:%M', title, msg)

    @reminder.command(aliases=['rm', 'month'])
    async def repeat_by_month(self, ctx, day: int, hour: int, minute: int, title, *, msg):
        await ctx.channel.purge(limit=1)
        if self.db['reminder'].find_one({"server": ctx.guild.id, "title": title}) is not None:
            await ctx.send(f'標題名稱相同，無法建立提醒')
            return
        setTime = datetime(2020, 1, day, hour=hour, minute=minute)
        await self.send_result(ctx, 'month', setTime, '%d%H%M', '每個月%d號 %H:%M', title, msg)

    @reminder.command(aliases=['o', 'once'])
    async def just_remind_once(self, ctx, year: int, month: int, day: int, hour: int, minute: int, *, msg):
        await ctx.channel.purge(limit=1)
        setTime = datetime(year, month, day, hour=hour, minute=minute, second=0)
        if datetime.now() > setTime:
            await ctx.send('時間不會回溯')
            return
        if datetime.now() + timedelta(days=30) < setTime:
            await ctx.send('不接受30天後的提醒')
        await self.send_result(ctx, 'none', setTime, '%Y%m%d%H%M', '%Y/%m/%d %H:%M', '提醒', msg)

    @reminder.command(aliases=['d', 'delete'])
    async def delete_reminders(self, ctx, title):
        await ctx.channel.purge(limit=1)
        query = {'server': ctx.guild.id, 'title': title}
        deletedItem = self.db['reminder'].delete_many(query)
        await ctx.send(f'{ctx.author.mention}刪除了 {deletedItem.deleted_count}個提醒')

    async def send_result(self, ctx, repeat, setTime, dbFormat, displayFormat, title, msg):
        query = {
            "server": ctx.guild.id,
            "channel": ctx.channel.id,
            "repeat": repeat,
            "time": setTime.strftime(dbFormat),
            "message": msg
        }
        if repeat == 'none':
            self.db['reminder'].insert_one(query)
        else:
            query["title"] = title
            self.db['reminder'].insert_one(query)
        embed = {
            "title": title,
            "description": '',
            "context": {
                "時間": setTime.strftime(displayFormat),
                "訊息": msg
            }
        }
        await ctx.send(f'{ctx.author.mention} 建立了一個提醒',
                       embed=setEmbedList(embed["title"], embed["description"], embed["context"]))


def setup(bot):
    bot.add_cog(Reminder(bot))
