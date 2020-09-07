from discord.ext import commands

from core.extension import Extension


class Leave(Extension):

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        self.invokedNoSubcommand(ctx)

    @leave.command(aliases=['l', 'list'])
    async def get_list(self, ctx):
        if ctx.invoked_subcommand is None:
            leave = self.db['config'].find_one({'server': ctx.message.guild.id})
            title = '離開訊息'
            description = ''
            context = {'通知頻道': '未設定' if leave["leave"]["channel"] == 0 else f'<#{leave["leave"]["channel"]}>',
                       '通知訊息': '未設定' if leave["leave"]["message"] == '' else leave["leave"]["message"]}
            await ctx.send(embed=self.setEmbedList(title, description, context))

    @leave.command(aliases=['c', 'channel'])
    async def set_channel(self, ctx, channelId: int):
        server = ctx.message.guild.id
        await ctx.channel.purge(limit=1)
        if self.isChannelInGuild(channelId, ctx.message.guild):
            self.db['config'].find_one_and_update({'server': server}, {'$set': {'leave.channel': channelId}})
            await ctx.send(f'**{ctx.message.guild}** 的離開訊息通知在 <#{channelId}>')
        elif channelId == 0:
            self.db['config'].find_one_and_update({'server': server}, {'$set': {'leave.channel': channelId}})
            await ctx.send(f'**{ctx.message.guild}** 的離開訊息通知已取消')
        else:
            await ctx.send(f'頻道ID輸入錯誤')

    @leave.command(aliases=['m', 'message'])
    async def set_message(self, ctx, *, msg):
        server = ctx.message.guild.id
        await ctx.channel.purge(limit=1)
        if self.db['config'].find_one({'server': server, 'leave.channel': 0}) is not None:
            await ctx.send(f'**!!!尚未設定離開訊息頻道!!!**')
        self.db['config'].find_one_and_update({'server': server}, {'$set': {'leave.message': msg}})
        await ctx.send(f'**{ctx.message.guild}** 的離開訊息通知為 {msg}')


def setup(bot):
    bot.add_cog(Leave(bot))
