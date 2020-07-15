import discord
from discord.ext import commands
from core.extension import Extension

ext_path = 'ext'
loadException = ('load','exceptions')

class Load(Extension):
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        if checkExtension(extension):
            return
        self.bot.load_extension(f'{ext_path}.{extension}')
        await ctx.send(f'loaded {extension} done.')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        if extension == 'load':
            return
        self.bot.unload_extension(f'{ext_path}.{extension}')
        await ctx.send(f'unloaded {extension} done.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        if extension == 'load':
            return
        self.bot.reload_extension(f'{ext_path}.{extension}')
        await ctx.send(f'reloaded {extension} done.')

    def checkExtension(extension):
        if extension is in loadException:
            print('Permission denied')
            return True
        return False

def setup(bot):
    bot.add_cog(Load(bot))