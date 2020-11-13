from discord.ext import commands

from core.extension import Extension
from core.util import invokedNoSubcommand, setEmbedList, isChannelInGuild


class GuildSetting(Extension):

    # ===== set welcome message ===== #

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        invokedNoSubcommand(ctx)

    @welcome.command(aliases=['l', 'list'])
    async def get_welcome_list(self, ctx):
        await self.get_list(ctx, 'welcome')

    @welcome.command(aliases=['c', 'channel'])
    async def set_welcome_channel(self, ctx, channelId: int):
        await self.set_channel(ctx, channelId, 'welcome')

    @welcome.command(aliases=['m', 'message'])
    async def set_welcome_message(self, ctx, *, msg):
        await self.set_message(ctx, msg, 'welcome')

    # ===== set leave message ====== #

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        invokedNoSubcommand(ctx)

    @leave.command(aliases=['l', 'list'])
    async def get_leave_list(self, ctx):
        await self.get_list(ctx, 'leave')

    @leave.command(aliases=['c', 'channel'])
    async def set_leave_channel(self, ctx, channelId: int):
        await self.set_channel(ctx, channelId, 'leave')

    @leave.command(aliases=['m', 'message'])
    async def set_leave_message(self, ctx, *, msg):
        await self.set_message(ctx, msg, 'leave')

    # ===== utils ===== #

    async def get_list(self, ctx, option):
        option_str = '歡迎' if option == 'welcome' else '離開'
        if ctx.invoked_subcommand is None:
            welcome = self.db['config'].find_one({'server': ctx.message.guild.id})
            title = f'{option_str}訊息'
            description = ''
            context = {
                f'{option_str}頻道': '未設定' if welcome[option]["channel"] == 0 else f'<#{welcome[option]["channel"]}>',
                f'{option_str}訊息': '未設定' if welcome[option]["message"] == '' else welcome[option]["message"]
            }
            await ctx.send(embed=setEmbedList(title, description, context))

    async def set_channel(self, ctx, channelId, option):
        option_str = '歡迎' if option == 'welcome' else '離開'
        server = ctx.message.guild.id
        await ctx.channel.purge(limit=1)
        if isChannelInGuild(channelId, ctx.message.guild):
            self.db['config'].find_one_and_update({'server': server}, {'$set': {f'{option}.channel': channelId}})
            await ctx.send(f'**{ctx.message.guild}** 的{option_str}訊息通知在 <#{channelId}>')
        elif channelId == 0:
            self.db['config'].find_one_and_update({'server': server}, {'$set': {f'{option}.channel': channelId}})
            await ctx.send(f'**{ctx.message.guild}** 的{option_str}訊息通知已取消')
        else:
            await ctx.send(f'頻道ID輸入錯誤')

    async def set_message(self, ctx, msg, option):
        option_str = '歡迎' if option == 'welcome' else '離開'
        server = ctx.message.guild.id
        await ctx.channel.purge(limit=1)
        if self.db['config'].find_one({'server': server, f'{option}.channel': 0}) is not None:
            await ctx.send(f'**!!!尚未設定{option_str}訊息頻道!!!**')
        self.db['config'].find_one_and_update({'server': server}, {'$set': {f'{option}.message': msg}})
        await ctx.send(f'**{ctx.message.guild}** 的{option_str}訊息通知為 {msg}')


def setup(bot):
    bot.add_cog(GuildSetting(bot))
