import discord
from discord.ext import commands
from pymongo import MongoClient
from core.extension import Extension

class Command(Extension):
    @commands.command()
    async def status(self, ctx):
        server = str(ctx.message.guild)
        owner = str(ctx.message.guild.owner.name)
        member_count = str(ctx.message.guild.member_count)
        online_member, dnd_member, idle_member  = 0, 0, 0 
        for member in ctx.guild.members:
            if str(member.status) != 'offline':
                online_member+=1
            if str(member.status) == 'dnd':
                dnd_member+=1
            if str(member.status) == 'idle':
                idle_member+=1
        embed=discord.Embed(title='樂高', description='不要踩會痛', color=0xff2600)
        embed.add_field(name='伺服器', value=server, inline=True)
        embed.add_field(name='創始者', value=owner, inline=True)
        embed.add_field(name='人數',value=member_count,inline=False)
        embed.add_field(name='線上',value=online_member,inline=True)
        embed.add_field(name='閒置',value=idle_member,inline=True)
        embed.add_field(name='勿擾',value=dnd_member,inline=True)
        embed.add_field(name='Ping', value= str(round(self.bot.latency*1000))+' ms', inline=True)
        embed.add_field(name='狀態', value='上線中', inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num:int):
        await ctx.channel.purge(limit = num+1)
        await ctx.send(f'{ctx.author.mention} 刪除了 {num} 則訊息')

    @commands.command()
    async def poll(self, ctx, question, *options: str):
        if len(options)>10:
            await ctx.send('你只能給10個選項')

        reactions = ('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟')
        description = []
        for x, option in enumerate(options):
            description += '\n\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title = question, color = 3553599, description = ''.join(description))
        embed.set_footer(text='發起者: {}'.format(ctx.author.name))
        await ctx.channel.purge(limit = 1)
        react_message = await ctx.send(embed = embed)

        for x, option in enumerate(options):
            await react_message.add_reaction(reactions[x])

def setup(bot):
    bot.add_cog(Command(bot))
    