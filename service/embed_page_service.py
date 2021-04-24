import asyncio
from datetime import datetime

from discord import Client, Reaction, Embed, Color
from discord.ext.commands import Context


class EmbedPageService:
    def __init__(self, title, data, color):
        self.embed_list = list()
        self.convert_data_to_embed(title, data, color)
        self.now_page = 1
        self.max_page = len(self.embed_list)
        self.message = None

    async def run(self, bot: Client, ctx: Context, delay=30):
        def check(reaction: Reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        self.message = await ctx.send('```資料查詢中...```')

        try:
            await self.send_page(self.now_page)
            while True:
                reaction, user = await bot.wait_for("reaction_add", timeout=delay, check=check)
                if str(reaction.emoji) == "▶️" and self.now_page != self.max_page:
                    await self.message.remove_reaction(reaction, user)
                    await self.send_page(self.now_page + 1)
                elif str(reaction.emoji) == "◀️" and self.now_page > 1:
                    await self.message.remove_reaction(reaction, user)
                    await self.send_page(self.now_page - 1)
                else:
                    await self.message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            pass
        await self.message.clear_reactions()
        await self.message.add_reaction('🚫')

    def convert_data_to_embed(self, title, data, color: Color):
        for fields in data:
            embed = Embed(title=title, color=color)
            for field in fields:
                embed.add_field(name=field['name'], value=field['value'], inline=False)
            self.embed_list.append(embed)

    async def send_page(self, page):
        self.now_page = page
        embed = self.embed_list[self.now_page - 1].copy()
        embed.set_footer(
            text=f'Page {self.now_page}/{self.max_page} • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        await self.message.edit(content=None, embed=embed)
        await self.message.add_reaction("◀️")
        await self.message.add_reaction("▶️")
