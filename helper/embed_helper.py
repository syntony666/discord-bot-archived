import asyncio

import discord
from discord.ext.commands import Context


class EmbedPage:
    def __init__(self, embed: discord.Embed, data: list, page_num: int):
        self.data = [data[i:i + page_num] for i in range(0, len(data), page_num)]
        self.embed = embed
        self.now_page = 1
        self.max_page = page_num

    def set_page(self, page):
        self.now_page = page
        self.embed.clear_fields()
        for key, value in self.data[self.now_page - 1].items():
            self.embed.add_field(name=key, value=value, inline=False)
        self.embed.set_footer(text=f'Page {self.now_page}/{self.max_page}')

    def run(self, bot: discord.Client, ctx: Context, delay=30):
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        self.set_page(self.now_page)
        message = await ctx.send(embed=self.embed)

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            if str(reaction.emoji) == "▶️" and self.now_page != self.max_page:
                self.set_page(self.now_page + 1)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and self.now_page > 1:
                self.now_page -= 1
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            message.clear_reactions()
            message.add_reaction('🚫')

