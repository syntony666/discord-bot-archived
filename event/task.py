import asyncio
from datetime import datetime

from core.database import Database
from core.extension import Extension
from dao.ban_dao import BanDAO
from dao.config_dao import ConfigDAO


class Task(Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        guild_id = int(Database('auth').get_data({"_id": "test"})[0]['guild_id'])

        async def run_task(method, sleep=1):
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                await asyncio.sleep(sleep)
                await method()

        async def remove_ban():
            guild = self.bot.get_guild(guild_id)
            if BanDAO().get_ban(unban=False) is not None:
                for ban in BanDAO().get_ban(unban=False):
                    member = guild.get_member(int(ban['member_id']))
                    if ban['end_time'] < datetime.now():
                        await member.remove_roles(
                            guild.get_role(ConfigDAO().get_ban_role()))
                        BanDAO().update_ban(ban['_id'], unban=True)
                    if ConfigDAO().get_ban_role() in member.roles:
                        BanDAO().update_ban(ban['_id'], unban=True)

        self.bot.loop.create_task(run_task(remove_ban))


def setup(bot):
    bot.add_cog(Task(bot))
