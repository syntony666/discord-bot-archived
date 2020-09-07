import discord
from discord.ext import commands
from core.extension import Extension


class Reply(Extension):

    @commands.group()
    async def reply(self, ctx):
        self.invokedNoSubcommand(ctx)

    @reply.command(aliases=['l', 'list'])
    async def get_list(self, ctx):
        if ctx.invoked_subcommand is None:
            server = ctx.message.guild.id
            await ctx.channel.purge(limit=1)
            embed = discord.Embed(title='回應列表', color=0xff2600)
            if self.db['reply'].find_one({'server': server}) is None:
                await ctx.send('**沒有回應列表**')
                return
            else:
                for x in self.db['reply'].find({'server': ctx.message.guild.id}):
                    embed.add_field(name=x['receive'], value=x['send'], inline=False)
            await ctx.send(embed=embed)

    @reply.command(aliases=['a', 'add'])
    async def add_reply(self, ctx, keyword, *, msg):
        server = ctx.message.guild.id
        found = self.db['reply'].find_one({'server': server, 'receive': keyword})
        await ctx.channel.purge(limit=1)
        if found is not None:
            self.db['reply'].find_one_and_update({'server': server, 'receive': keyword}, {'$set': {'send': msg}})
            await ctx.send(f'{ctx.author.mention} 教我把 **{keyword}** 的回答改成 **{msg}**')
            return
        self.db['reply'].insert({'server': server, 'receive': keyword, 'send': msg})
        await ctx.send(f'{ctx.author.mention} 教我聽到人家說 **{keyword}** 要回答 **{msg}**')

    @reply.command(aliases=['d', 'delete'])
    async def delete_reply(self, ctx, keyword):
        server = ctx.message.guild.id
        found = self.db['reply'].find_one({'server': server, 'receive': keyword})
        await ctx.channel.purge(limit=1)
        if found is not None:
            self.db['reply'].find_one_and_delete({'server': server, 'receive': keyword})
            await ctx.send(f'{ctx.author.mention} 當你說 **{keyword}** 時候 我不會理你')
            return
        await ctx.send(f'{ctx.author.mention} 沒人叫我聽到 **{keyword}** 的時候要回答')


def setup(bot):
    bot.add_cog(Reply(bot))
