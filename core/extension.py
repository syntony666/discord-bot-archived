import discord
from discord.ext import commands

class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'{ext_path}.{name}')
    await ctx.send(f'loaded {extension} done.')

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'{ext_path}.{name}')
    await ctx.send(f'unloaded {extension} done.')

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f'{ext_path}.{name}')
    await ctx.send(f'reloaded {extension} done.')