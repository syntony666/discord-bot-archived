from discord.ext import commands

from core.extension import Extension


class Help(Extension):
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.sendHelper(ctx, 'help')

    @help.command()
    async def reply(self, ctx):
        await self.sendHelper(ctx, 'reply')

    @help.command()
    async def welcome(self, ctx):
        await self.sendHelper(ctx, 'welcome')

    @help.command()
    async def leave(self, ctx):
        await self.sendHelper(ctx, 'leave')

    async def sendHelper(self, ctx, command):
        helper = self.db['help'].find_one({'ext': command})
        await ctx.send(embed=self.setEmbedList(helper['title'], helper['description'], helper['context']))


def setup(bot):
    bot.add_cog(Help(bot))
