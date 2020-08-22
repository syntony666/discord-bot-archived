import discord
from discord.ext import commands
from pymongo import MongoClient
from core.extension import Extension

class Welcome(Extension):

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        if ctx.invoked_subcommand == None:
            title = '指令說明 (歡迎訊息)'
            description = '只有管理員能修改'
            context = {
                '列表':'>welcome l', 
                '新增':'>welcome a [頻道ID] [訊息內容]',
                '修改':'>welcome s c [頻道ID]\n>welcome s m [訊息內容]',
                '刪除':'>welcome d'}
            await ctx.send(embed=self.setEmbedList(title, description, context))
    
    @welcome.command()
    async def l(self, ctx):
        server = ctx.message.guild.id
        found = self.db['welcome'].find_one({'server' : server})
        await ctx.channel.purge(limit = 1)
        if found is None:
            await ctx.send(f'**{ctx.message.guild}** 未設定歡迎訊息')
            return
        embed=discord.Embed(title='歡迎訊息',description=f'{found["message"]}\n在 <#{found["channel"]}>', color=0xff2600)
        await ctx.send(embed=embed)

    @welcome.command()
    async def a(self, ctx, channel, *, msg):
        server = ctx.message.guild.id
        found = self.db['welcome'].find_one({'server' : server})
        await ctx.channel.purge(limit = 1)
        if found is not None:
            await ctx.send(f'**{ctx.message.guild}** 已存在歡迎訊息，請使用 >welcome s 更改')
            return
        self.db['welcome'].insert({'server' : server, 'channel': channel, 'message': msg})
        embed=discord.Embed(title='已設定歡迎訊息',description=f'{msg}\n在 <#{channel}>', color=0xff2600)
        await ctx.send(embed=embed)

    @welcome.command()
    async def s(self, ctx, option, *, arg):
        server = ctx.message.guild.id
        found = self.db['welcome'].find_one({'server' : server})
        await ctx.channel.purge(limit = 1)
        if found is None:
            await ctx.send(f'**{ctx.message.guild}** 未設定歡迎訊息')
            return
        if option == 'c':
            self.db['welcome'].find_one_and_update({'server' : server},{'$set':{'channel': arg}})
            await ctx.send(f'**{ctx.message.guild}** 的歡迎訊息通知在 <#{arg}>')
        elif option == 'm':
            self.db['welcome'].find_one_and_update({'server' : server},{'$set':{'message': arg}})
            await ctx.send(f'**{ctx.message.guild}** 的歡迎訊息為 **{arg}**')
        else:
            raise commands.errors.CommandNotFound

    @welcome.command()
    async def d(self, ctx):
        server = ctx.message.guild.id
        found = self.db['welcome'].find_one({'server' : server})
        await ctx.channel.purge(limit = 1)
        if found is not None:
            self.db['welcome'].find_one_and_delete({'server' : server})
            await ctx.send(f'已刪除歡迎訊息')
            return
        await ctx.send(f'你還沒設定，我刪不掉')
        

def setup(bot):
    bot.add_cog(Welcome(bot))