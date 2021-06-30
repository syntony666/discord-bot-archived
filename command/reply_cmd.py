import os
from datetime import datetime

from discord import Client, Color, File, Embed
from discord.ext import commands

from core.exception import DataExist, DataNotExist
from core.extension import Extension
from dao.reply_dao import ReplyDao
from model.reply_model import ReplyModel
from service.embed_page_service import EmbedPageService


class Reply(Extension):
    def __init__(self, bot: Client):
        super(Reply, self).__init__(bot)
        self.embed_color = Color.blue()
        self.reply_dao = ReplyDao()

    @commands.group()
    async def reply(self, ctx: commands.Context):
        pass

    @reply.command(aliases=['a'])
    async def set_reply(self, ctx: commands.Context, receive: str, *, send: str):
        embed_title = ''
        guild_id = str(ctx.guild.id)
        if len(receive) > 200 or len(send) > 1000:
            await ctx.send('```字數限制：關鍵字200字內，回應1000字內```')
            return
        try:
            self.reply_dao.create_data(guild_id, receive, send)
            embed_title = "已新增回應"
        except DataExist:
            self.reply_dao.update_data(guild_id, receive, send)
            embed_title = "已修改回應"
        finally:
            response = self.reply_dao.get_data(guild_id, receive)
            await send_embed_msg(ctx, embed_title, response[0], self.embed_color)

    @reply.command(aliases=['l'])
    async def get_reply(self, ctx):
        guild_id = str(ctx.guild.id)
        reply_list = self.reply_dao.get_data(guild_id)
        if len(reply_list) == 0:
            embed = Embed(title='__回應列表__', color=Color.green())
            embed.description = '查無資料'
            await ctx.send(embed=embed)
            return
        reply_list = [{'name': x.receive, 'value': x.send} for x in reply_list]
        embed_page_service = EmbedPageService(
            '__回應列表__',
            [reply_list[x:x + 10] for x in range(0, len(reply_list), 10)],
            Color.green()
        )
        await embed_page_service.run(self.bot, ctx)

    @reply.command(aliases=['s'])
    async def search_reply(self, ctx, receive):
        guild_id = str(ctx.guild.id)
        reply_list = self.reply_dao.search_data(guild_id, receive)
        if len(reply_list) == 0:
            embed = Embed(title='__回應列表__', color=Color.green())
            embed.description = '查無資料'
            await ctx.send(embed=embed)
            return
        reply_list = [{'name': x.receive, 'value': x.send} for x in reply_list]
        embed_page_service = EmbedPageService(
            '__回應列表__',
            [reply_list[x:x + 10] for x in range(0, len(reply_list), 10)],
            Color.green()
        )
        await embed_page_service.run(self.bot, ctx)

    @reply.command(aliases=['file'])
    async def get_reply_file(self, ctx):
        filename = 'reply.json'
        guild_id = str(ctx.guild.id)
        reply_list = self.reply_dao.get_data(guild_id)
        f = open(filename, "w", encoding="utf-8")
        f.write("{\n")
        for x in reply_list:
            f.write(f'\t"{x.receive}" : "{x.send}",\n')
        f.write('}')
        f.close()
        reply_file = File(filename, filename=filename)
        await ctx.send(file=reply_file)
        os.remove(filename)


    @reply.command(aliases=['d'])
    async def delete_reply(self, ctx: commands.Context, receive):
        guild_id = str(ctx.guild.id)
        try:
            response = self.reply_dao.get_data(guild_id, receive)
            self.reply_dao.del_data(guild_id, receive)
            await send_embed_msg(ctx, '已刪除回應', response[0], Color.red())
        except DataNotExist:
            response = ReplyModel(guild_id, receive, '__*查無資料*__')
            await send_embed_msg(ctx, '無回應可刪除', response, Color.red())


async def send_embed_msg(ctx: commands.Context, title, response: ReplyModel, color):
    reply_thumbnail = File(
        'src/img/reply_thumbnail.png', filename='reply_thumbnail.png')
    embed = Embed(title=title, color=color)
    embed.set_thumbnail(url='attachment://reply_thumbnail.png')
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name='**觸發回覆**', value=response.receive, inline=False)
    embed.add_field(name='**回應內容**', value=response.send, inline=False)
    await ctx.send(file=reply_thumbnail, embed=embed)


def setup(bot):
    bot.add_cog(Reply(bot))
