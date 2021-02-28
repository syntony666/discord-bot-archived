import asyncio

import discord


class EmbedPage:
    def __init__(self, embed: discord.Embed, data: list, page_num: int):
        self.data = [data[i:i + page_num] for i in range(0, len(data), page_num)]
        self.embed = embed
        self.now_page = 1
        self.max_page = len(data)

    def set_page(self, page):
        self.now_page = page
        self.embed.clear_fields()
        for x in self.data[self.now_page - 1]:
            self.embed.add_field(name=x['key'], value=x['value'], inline=False)
        self.embed.set_footer(text=f'Page {self.now_page}/{self.max_page}')

    async def run(self, bot: discord.Client, ctx, delay=30):
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        self.set_page(self.now_page)
        message = await ctx.send(embed=self.embed)

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        try:
            while True:
                reaction, user = await bot.wait_for("reaction_add", timeout=delay, check=check)
                if str(reaction.emoji) == "▶️" and self.now_page != self.max_page:
                    self.set_page(self.now_page + 1)
                    await message.remove_reaction(reaction, user)
                    await message.edit(embed=self.embed)
                elif str(reaction.emoji) == "◀️" and self.now_page > 1:
                    self.set_page(self.now_page - 1)
                    await message.remove_reaction(reaction, user)
                    await message.edit(embed=self.embed)
                else:
                    await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            message.clear_reactions()
            message.add_reaction('🚫')

