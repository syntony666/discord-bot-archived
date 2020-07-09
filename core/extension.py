import discord
from discord.ext import commands

class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        bot.load_extension(f'{ext_path}.{name}')
        await ctx.send(f'loaded {extension} done.')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        bot.unload_extension(f'{ext_path}.{name}')
        await ctx.send(f'unloaded {extension} done.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        bot.reload_extension(f'{ext_path}.{name}')
        await ctx.send(f'reloaded {extension} done.')