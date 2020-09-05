from discord.ext import commands

from core.extension import Extension


class Event(Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f'{message.author}({message.guild}, #{message.channel}): ')
        print(message.content)
        if message.author == self.bot.user:
            return
        found = self.db['reply'].find_one({'server': message.guild.id, 'receive': message.content})
        if found is not None:
            await message.channel.send(found['send'])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome = self.db['config'].find_one({'server': member.guild.id})
        if welcome["leave"]["channel"] != 0:
            await self.bot.get_channel(welcome["leave"]["channel"])\
                .send(f'{member} {welcome["leave"]["message"]}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcome = self.db['config'].find_one({'server': member.guild.id})
        if welcome["welcome"]["channel"] != 0:
            await self.bot.get_channel(welcome["welcome"]["channel"])\
                .send(f'{member.mention} {welcome["welcome"]["message"]}')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        configData = {
            'server': guild.id,
            'welcome': {'channel': 0, 'message': ''},
            'leave': {'channel': 0, 'message': ''}
        }
        self.db['config'].insert(configData)

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


def setup(bot):
    bot.add_cog(Event(bot))
