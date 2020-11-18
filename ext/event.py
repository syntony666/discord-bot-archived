import asyncio
from datetime import datetime

from discord.ext import commands

from core.extension import Extension
from core.util import get_all_command
from ext.member_info import message_exp, message_count
from ext.reply import reply_process


class Event(Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f'Ready!',
            f'Logged in as ---->{self.bot.user}',
            f'ID:   {self.bot.user.id}',
            f'Time: {datetime.now()}',
            f'Ping: {round(self.bot.latency * 1000)} ms\n',
            sep='\n'
        )
        print(f'Guilds Connected: ')
        for guild in self.bot.guilds:
            print(guild.name)
        print()

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f'{message.author}({message.guild}, #{message.channel}): ')
        print(message.content)
        if message.author != self.bot.user:
            await reply_process(self.db, message)
            await asyncio.sleep(1)
            message_count(message.author)
            if all('>' + x not in message.content for x in get_all_command(self.bot)):
                message_exp(message.author)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        query = {
            'server': payload.guild_id,
            'message_id': payload.message_id,
            'emoji': str(payload.emoji)
        }
        reaction_role = self.db['role-setting'].find_one(query)
        if reaction_role is not None:
            await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(reaction_role['role']))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        query = {
            'server': payload.guild_id,
            'message_id': payload.message_id,
            'emoji': str(payload.emoji)
        }
        reaction_role = self.db['role-setting'].find_one(query)
        if reaction_role is not None:
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(reaction_role['role']))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome = self.db['config'].find_one({'server': member.guild.id})
        if welcome["welcome"]["channel"] != 0:
            await self.bot.get_channel(welcome["welcome"]["channel"]) \
                .send(f'{member.mention} {welcome["welcome"]["message"]}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcome = self.db['config'].find_one({'server': member.guild.id})
        if welcome["leave"]["channel"] != 0:
            await self.bot.get_channel(welcome["leave"]["channel"]) \
                .send(f'**{member}** {welcome["leave"]["message"]}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        configData = {
            'server': guild.id,
            'welcome': {'channel': 0, 'message': ''},
            'leave': {'channel': 0, 'message': ''}
        }
        self.db['config'].insert_one(configData)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        serverData = {'server': guild.id}
        self.db['config'].find_one_and_delete(serverData)
        self.db['reply'].delete_many(serverData)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send('你想對我做什麼 我好害怕 QQ')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('欸！ 你話沒講完就想跑啊')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('你沒權限給我下去!!!!!')
        else:
            await ctx.send(f'```\n{str(error)}\n```')


def setup(bot):
    bot.add_cog(Event(bot))
