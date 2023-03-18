import discord
from discord.ext import commands
from discord.ui import Button, View

from modules.chatgptApi import gpt_engine
from modules.woodenFish.wood_fish_engine import *

with open("info.json", 'r') as f:
    bot_info = json.load(f)

INT = discord.Intents.default()
INT.message_content = True
client = commands.Bot(command_prefix='$', intents=INT)

count = 0


@client.command(name='knock')
async def knock(ctx: commands.context.Context):
    async def again_callback(interaction: discord.Interaction):
        tname = interaction.user
        tuid = interaction.user.id
        tuid = str(tuid)
        rval = process(tuid)

        embed = discord.Embed(title="电子木鱼", description=f"获得了{rval}点功德", color=0xff5757)
        embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
        embed.add_field(name=f"{tname} 当前功德", value=f"{database[str(tuid)]['honor']}", inline=False)

        if database[tuid]['broken']:
            embed.add_field(name=f"木鱼损坏！！", value=f"0", inline=False)

        await interaction.response.send_message(embed=embed, view=view)

    async def replace_callback(interaction: discord.Interaction):
        tname = interaction.user
        tuid = interaction.user.id
        tuid = str(tuid)
        res = replace_wf(tuid)
        if res:
            embed = discord.Embed(title="电子木鱼", description=f"已替换新木鱼", color=0xff5757)
            embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
            embed.add_field(name=f"{tname} 当前功德", value=f"{database[str(tuid)]['honor']}", inline=True)

            await interaction.response.send_message(embed=embed, view=view)
        else:
            embed = discord.Embed(title="电子木鱼", description=f"木鱼没有坏！-100功德！", color=0xff5757)
            embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
            embed.add_field(name=f"{tname} 当前功德", value=f"{database[str(tuid)]['honor']}", inline=True)

            await interaction.response.send_message(embed=embed, view=view)

    uid = ctx.author.id
    uid = str(uid)
    rval = process(uid)

    again = Button(label="敲一下", style=discord.ButtonStyle.blurple)
    again.callback = again_callback

    replace = Button(label="替换新木鱼", style=discord.ButtonStyle.blurple)
    replace.callback = replace_callback

    view = View()
    view.add_item(again)
    view.add_item(replace)

    embed = discord.Embed(title="电子木鱼", description=f"获得了{rval}点功德", color=0xff5757)
    embed.set_thumbnail(url="https://static5.qiang100.com/images/zhuanti-icon2/original/400/muyu4.jpg")
    embed.add_field(name=f"{ctx.message.author} 当前功德", value=f"{database[str(uid)]['honor']}", inline=False)
    if database[uid]['broken']:
        embed.add_field(name=f"木鱼损坏！！", value=f"0", inline=False)

    await ctx.send(embed=embed, view=view)


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


@client.command(name='gpt')
async def stat(ctx: commands.context.Context, *args):
    uid = ctx.author.id
    p = " ".join(args)

    res = gpt_engine(p, uid) + "\n\n------ Generated by gpt-3.5-turbo ------"

    await ctx.reply(content=res)


try:
    while True:
        client.run(bot_info['token'])
except RuntimeError or Exception as e:
    print(e)
    for i in database:
        f = open(f'./data/{i}.json', 'w')
        json.dump(database[i], f)
    exit()