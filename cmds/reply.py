from datetime import datetime

import discord
from discord.ext import commands

from core.exception import DataExist, DataNotExist
from core.extension import Extension
from dao.reply_dao import ReplyDAO
from helper.embed_helper import EmbedPage


class Reply(Extension):
    def __init__(self, bot: discord.Client):
        super().__init__(bot)
        self.embed_color = discord.Color.blue()

    @commands.group()
    async def reply(self, ctx):
        pass

    @reply.command(aliases=['a'])
    async def set_reply(self, ctx, receive, *, send):
        embed_title = ''
        if len(receive) > 200 or len(send) > 1000:
            await ctx.send('```字數限制：關鍵字200字內，回應1000字內```')
        try:
            ReplyDAO().create_reply(receive, send)
            embed_title = "已新增回應"
        except DataExist:
            ReplyDAO().update_reply(receive, send)
            embed_title = "已修改回應"
        finally:
            response = ReplyDAO().get_reply(receive)
            await send_embed_msg(ctx, embed_title, response, discord.Color.blue())

    @reply.command(aliases=['s'])
    async def search(self, ctx, keyword):
        reply_list = ReplyDAO().get_reply(f'/{keyword}/')
        embed = discord.Embed(title=f'*{keyword}* 搜尋結果', color=discord.Color.green())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(reply_list) == 0:
            embed.description = '查無結果'
            await ctx.send(embed=embed)
            return
        reply_list = [{'key': x['_id'], 'value': x['value']} for x in reply_list]
        embed_page = EmbedPage(embed, reply_list, 8)
        await embed_page.run(self.bot, ctx)

    @reply.command(aliases=['l'])
    async def get_reply(self, ctx):
        reply_list = ReplyDAO().get_reply()
        if len(reply_list) == 0:
            await ctx.send('**沒有回應列表**')
            return
        embed = discord.Embed(title='__回應列表__', color=discord.Color.green())
        reply_list = [{'key': x['_id'], 'value': x['value']} for x in reply_list]
        embed_page = EmbedPage(embed, reply_list, 8)
        await embed_page.run(self.bot, ctx)

    @reply.command(aliases=['d'])
    async def delete_reply(self, ctx, receive):
        try:
            response = ReplyDAO().del_reply(receive)
            await send_embed_msg(ctx, '已刪除回應', response, discord.Color.red())
        except DataNotExist:
            response = {
                '_id': receive,
                'value': '__*查無資料*__'
            }
            await send_embed_msg(ctx, '無回應可刪除', response, discord.Color.red())


async def send_embed_msg(ctx, title, response, color):
    reply_thumbnail = discord.File(
        'src/img/reply_thumbnail.png', filename='reply_thumbnail.png')
    embed = discord.Embed(title=title, color=color)
    embed.set_thumbnail(url='attachment://reply_thumbnail.png')
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name=response['_id'], value=response['value'])
    await ctx.send(file=reply_thumbnail, embed=embed)


def setup(bot):
    bot.add_cog(Reply(bot))
