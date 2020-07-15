import discord
from discord.ext import commands
from pymongo import MongoClient
from core.extension import Extension

class Event(Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->' , self.bot.user)
        print('ID:', self.bot.user.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f'{message.author}({message.guild}, #{message.channel}): ')
        print(message.content)
        if message.author == self.bot.user:
            return
        found = self.db['keywords'].find_one({'server' : str(message.guild.id), 'receive': str(message.content)})
        if found is not None:
            await message.channel.send(found['send'])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = self.db['welcome'].find_one({'server': str(member.guild.id)})
        await self.bot.get_channel(int(msg['channel'])).send(f'{member.mention} {msg["message"]}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send('你想對我做什麼 我好害怕 QQ')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('欸！ 你話沒講完就想跑啊')
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send('你沒權限給我下去!!!!!')

def setup(bot):
    bot.add_cog(Event(bot))