from datetime import datetime

import discord
from discord.ext import commands

from core.exception import DataExist, DataNotExist
from core.extension import Extension
from dao.reply_dao import ReplyDAO


class Reply(Extension):
    def __init__(self, bot: discord.Client):
        super().__init__(bot)
        self.reply_thumbnail = discord.File('src/img/reply_thumbnail.png', filename='reply_thumbnail.png')

    @commands.group()
    async def reply(self, ctx):
        pass

    @reply.command(aliases=['a'])
    async def set_reply(self, ctx, receive, *, send):
        embed_title = ''
        try:
            ReplyDAO().create_reply(receive, send)
            embed_title = "已新增回應"
        except DataExist:
            ReplyDAO().update_reply(receive, send)
            embed_title = "已修改回應"
        finally:
            response = ReplyDAO().get_reply(receive)
            embed = discord.Embed(title=embed_title)
            embed.set_thumbnail(url='attachment://reply_thumbnail.png')
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            embed.add_field(name=response['_id'], value=response['value'])
            await ctx.send(file=self.reply_thumbnail, embed=embed)

    @reply.command(aliases=['l'])
    async def get_reply(self, ctx):
        reply_list = ReplyDAO().get_reply()
        if len(reply_list) == 0:
            await ctx.send('**沒有回應列表**')
            return
        embed = discord.Embed(title='__回應列表__', color=0x3ea076)
        reply_list = [reply_list[i:i + 10] for i in range(0, len(reply_list), 10)]
        for y in reply_list:
            for x in y:
                embed.add_field(name=x['_id'], value=x['value'], inline=False)
            await ctx.send(embed=embed)
            embed.clear_fields()

    @reply.command(aliases=['d'])
    async def delete_reply(self, ctx, receive):
        try:
            ReplyDAO().del_reply(receive)
            await ctx.send(
                f'{ctx.author.mention} 叫我聽到 **{receive}** 的時候不要回應，存在感-1 QAQ')
        except DataNotExist:
            await ctx.send(
                f'{ctx.author.mention} 沒人叫我聽到 **{receive}** 的時候要回應，你是不是想騙！')


def setup(bot):
    bot.add_cog(Reply(bot))
