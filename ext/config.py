from discord.ext import commands

from core.extension import Extension


class Config(Extension):

    @commands.group()
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            title = '指令說明 (頻道設定)'
            description = '只有管理員能修改'
            context = {
                '歡迎訊息設定':
                    '修改發送頻道: >config welcome c [頻道ID](設定為0時則取消)\n'
                    '修改發送訊息: >config welcome m [訊息內容]',
                '離開訊息設定':
                    '修改發送頻道: >config welcome c [頻道ID](設定為0時則取消)\n'
                    '修改發送訊息: >config welcome m [訊息內容]'
            }
            await ctx.send(embed=self.setEmbedList(title, description, context))


def setup(bot):
    bot.add_cog(Config(bot))
