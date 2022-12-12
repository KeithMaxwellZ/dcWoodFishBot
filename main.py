import asyncio
import json
import discord
from discord.ext import commands
from discord.ui import Button, View

from wood_fish_engine import *

with open("info.json", 'r') as f:
    bot_info = json.load(f)

INT = discord.Intents.default()
INT.message_content = True
client = commands.Bot(command_prefix='$', intents=INT)

count = 0


@client.command(name='knock')
async def knock(ctx: commands.context.Context):
    def gen_embed(author_name, val, inc):
        embed = discord.Embed(title="电子木鱼", description=f"获得了{inc}点功德", color=0xff5757)
        embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
        embed.add_field(name=f"{author_name} 当前功德", value=f"{val}", inline=True)

        return embed

    async def btn_callback(interaction: discord.Interaction):
        tname = interaction.user
        tuid = interaction.user.id
        tuid = str(tuid)
        rval = process(tuid)
        await interaction.response.send_message(embed=gen_embed(tname, database[str(tuid)]['honor'], rval), view=view)

    uid = ctx.author.id
    uid = str(uid)
    rval = process(uid)

    btn = Button(label="敲一下", style=discord.ButtonStyle.blurple)
    btn.callback = btn_callback
    view = View()
    view.add_item(btn)
    await ctx.send(embed=gen_embed(ctx.message.author, database[str(uid)]['honor'], rval), view=view)


@client.command(name='draw')
async def draw(ctx: commands.context.Context):
    uid = ctx.author.id
    uid = str(uid)

    if database[uid]['honor'] < 1000:
        await ctx.send(content='您的功德不足')
    else:
        res = recruit(uid, 10)
        embed = discord.Embed(title="电子木鱼", description=f"招募结果", color=0xff5757)
        embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
        embed.add_field(name="当前功德", value=database[uid]['honor'], inline=False)
        for x in range(len(res)):
            embed.add_field(name=text[x], value=res[x], inline=False)

        await ctx.send(embed=embed)


@client.command(name='rank')
async def rank(ctx: commands.context.Context):
    lst = get_rank()

    embed = discord.Embed(title="电子木鱼", description=f"功德无量", color=0xff5757)
    embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
    for x in lst:
        print(x)
        embed.add_field(name=ctx.guild.get_member(int(x[0])), value=x[1], inline=False)

    await ctx.send(embed=embed)


@client.command(name='stat')
async def stat(ctx: commands.context.Context):
    uid = ctx.author.id
    uid = str(uid)

    lst = get_stats(uid)
    embed = discord.Embed(title="电子木鱼", description=f"我的寺庙", color=0xff5757)
    embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
    for x in range(len(lst)):
        embed.add_field(name=text[x], value=lst[x], inline=False)

    await ctx.send(embed=embed)


try:
    while True:
        client.run(bot_info['token'])
except RuntimeError or Exception as e:
    print(e)
    for i in database:
        f = open(f'./data/{i}.json', 'w')
        json.dump(database[i], f)
    exit()
