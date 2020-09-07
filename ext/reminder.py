import asyncio
import datetime

from datetime import datetime

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
    async def repeat_by_day(self, ctx, hour: int, minute: int, title, *, msg):
        self.db['reminder'].insert_one({
            "server": ctx.guild.id,
            "channel": ctx.channel.id,
            "repeat": "day",
            "time": datetime(2020, 1, 1, hour=hour, minute=minute).strftime('%d%H%M'),
            "title": title,
            "message": msg
        })

    @reminder.command(aliases=['rm', 'month'])
    async def repeat_by_month(self, ctx, day: int, hour: int, minute: int, title, *, msg):
        self.db['reminder'].insert_one({
            "server": ctx.guild.id,
            "channel": ctx.channel.id,
            "repeat": "month",
            "time": datetime(2020, 1, day, hour=hour, minute=minute).strftime('%H%M'),
            "title": title,
            "message": msg
        })

    @reminder.command(aliases=['o', 'once'])
    async def just_remind_once(self, ctx, year: int, month: int, day: int, hour: int, minute: int, title, *, msg):
        setTime = datetime(year, month, day, hour=hour, minute=minute, second=0)
        if datetime.now() > setTime:
            await ctx.send('時間不會回溯')
            return
        self.db['reminder'].insert_one({
            "server": ctx.guild.id,
            "channel": ctx.channel.id,
            "repeat": "none",
            "time": setTime.strftime('%Y%m%d%H%M'),
            "title": title,
            "message": msg
        })

    @reminder.command(alias=['d', 'delete'])
    async def delete_reminders(self, ctx, title):
        query = {'server': ctx.guild.id, "title": title}
        self.db['reminder'].delete_many(query)


def setup(bot):
    bot.add_cog(Reminder(bot))
