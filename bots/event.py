import discord
from discord.ext import commands
from pymongo import MongoClient
from extension import Extension

db = MongoClient('mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq').heroku_vfz6lbdq

welcome, keywords = db['welcome'], db['keywords']

class Event(Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author == self.bot.user:
            return
        found = keywords.find_one({'server' : str(message.guild.id), 'receive': str(message.content)})
        if found is not None:
            await message.channel.send(found['send'])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        msg = welcome.find({'server': str(member.guild.id)})
        await self.bot.get_channel(int(msg['channel'])).send(msg['message'])

def setup(bot):
    bot.add_cog(Event(bot))