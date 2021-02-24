from datetime import datetime

from discord.ext import commands

from core.extension import Extension


class Event(Extension):

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f'Ready!',
            f'Log as ---> {self.bot.user}',
            f'ID:   {self.bot.user.id}',
            f'Time: {datetime.now()}',
            f'Ping: {round(self.bot.latency * 1000)} ms',
            sep='\n'
        )


def setup(bot):
    bot.add_cog(Event(bot))
