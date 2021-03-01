import asyncio

import discord


class EmbedPage:
    def __init__(self, embed: discord.Embed, data: list, page_num: int):
        self.data = [data[i:i + page_num] for i in range(0, len(data), page_num)]
        self.embed = embed
        # self.embed = list()
        # print(len(self.data))
        # for n in range(len(self.data)):
        #     self.embed.append(embed)
        #     for x in self.data[n]:
        #         self.embed[n].add_field(name=x['key'], value=x['value'], inline=False)
        #     print(self.embed[n].to_dict())
        self.now_page = 1
        self.max_page = len(self.data)
        self.message = None

    def set_page(self, page):
        self.now_page = page
        embed = self.embed.copy()
        for x in self.data[self.now_page - 1]:
            embed.add_field(name=x['key'], value=x['value'], inline=False)
        embed.set_footer(text=f'Page {self.now_page}/{self.max_page}')
        return embed

    async def set_new_message(self, ctx):
        self.set_page(self.now_page)
        self.message = await ctx.send(embed=self.embed)
        await self.message.add_reaction("◀️")
        await self.message.add_reaction("▶️")

    async def change_page(self, ctx, page, reaction, user):
        try:
            embed = self.set_page(page)
            await self.message.remove_reaction(reaction, user)
            await self.message.edit(embed=embed)
        except discord.errors.HTTPException:
            await self.message.delete()
            await self.set_new_message(ctx)

    async def run(self, bot: discord.Client, ctx, delay=30):
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        await self.set_new_message(ctx)

        try:
            while True:
                reaction, user = await bot.wait_for("reaction_add", timeout=delay, check=check)
                if str(reaction.emoji) == "▶️" and self.now_page != self.max_page:
                    await self.change_page(ctx, self.now_page + 1, reaction, user)
                elif str(reaction.emoji) == "◀️" and self.now_page > 1:
                    await self.change_page(ctx, self.now_page + 1, reaction, user)
                else:
                    await self.message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await self.message.clear_reactions()
            await self.message.add_reaction('🚫')
