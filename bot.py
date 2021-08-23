"""

这是一个作于办公的discord小机器人，需要用到以下的库:
discord.py prettytable (用于后续详细timetable)
安装后根据我的注释修改你需要的功能即可啦~
Author: Rick

"""

import asyncio
import json

import discord
import discord.utils
import requests
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents, command_prefix='$') #command key with "$",$进行command


# 登陆机器人成功所显示内容
@client.event
async def on_ready():
    print('Logged on as', client.user)
    client.loop.create_task(status_task())


# 此部分用于新成员加入时，机器人自动进行欢迎回复
@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        # 以下内容可根据需要进行更改~
        embed = discord.Embed(title=f"欢迎你, {member.name}",
                              description="欢迎来到Creader大家庭,我是旺财弟弟,我叫西八，想聊天请@我哦 汪!")
        embed.set_thumbnail(url=member.avatar_url)  # 用户头像
        # ----------------------
        await guild.system_channel.send(embed=embed)
        # 发送一个工号DM
        await send_dm(context="Null", user=member, message="欢迎你哟，您在Creader的工号：#" + str(guild.member_count))
        print('The New Member Join:', member.name) #后端显示新成员加入


# ------------------------------------API PART ----------------------------------------------------------

# 随机的机器人状态 自己在await client.change_presence()里面的内容修改要随机出现的状态哦~
# TODO 写入随机出现状态,目前该方式有点浪费系统资源
async def status_task():
    while True:  # status有在线(online), 请勿打扰(dnd),离开(leave)等，自己选.
        await client.change_presence(status=discord.Status.online, activity=discord.Game("炒狗狗币"))
        print('Bot status switch to: "炒狗狗币"')
        await asyncio.sleep(300)  # 这个地方更改每次刷新的时间哦~单位为秒
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game("啃办公室家具"))
        print('Bot status switch to: "啃办公室家具"')
        await asyncio.sleep(300)
        await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name="西八犬的故事",
              url="https://www.youtube.com/watch?v=XHZHU9Df4Go&list=PLSMd0TuMYBgrt1g5hWt_YsUuurRzf2IJ_&index=35"))
        print('Bot status switch to: "西八犬的故事"')
        await asyncio.sleep(300)


# TODO 整合API进入单独的.py中
# 发送DM的API
async def send_dm(context, user: discord.User, message):
    await user.send(message)
    #后端显示DM发送
    print ("The DM been send to: " + user + "Context: " + message)


# TODO 移动成员API
def move_member(user_id,channel_id):
    await client.move_member(user_id, channel_id)

# TODO 创建私人频道API
#async def create_pra_chan(name,category):
#    name = ctx.message.author
#    category = discord.CategoryChannel.id =
#   await guild.create_text_channel(str(name), overwrites=overwrites, category=category)
#TODO 创建并随机分配房间ID



# https://api.qingyunke.com/ 提供API支持
# TODO AI随机回复API
@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        context = message.content
        context.replace("<> ","") #需要把之前@机器人的内容去除,此地方为机器人的ID
        response = json.loads(requests.get("https://api.qingyunke.com/api.php?key=free&appid=0&msg="+context).text)
        text = response["content"] + ",汪~"
        #替换API机器人原始的名字至您要的名字
        new_text = text.replace("菲菲","西八")
        #后端回复记录
        print("The Bot been mention, will do auto response: ")
        print("context: " + new_text)
        await message.channel.send(new_text)

#TODO 已完成表格设计，需要通过输出csv或者mysql来进行记录
#TIMA-TABLE FORMAT：
#[预约时间] [预约人] [预约会议室ID] [会议成员] [结束时间] (IN LIST)
DATASET = []
s = ['房间ID  开始时间  主持人   人数   结束时间']
final_table = ""
def add_table(time, holder, mtID, members, end):
    DATASET.append((time, holder, mtID, members, end))
    for data in DATASET:
        s.append('   '.join([str(item).center(5, ' ') for item in data]))
    global final_table
    DATASET.pop(0)
    final_table = '```' + '\n'.join(s) + '```'

#预约meeting room:
@client.event
async def on_message(message):
    if message.content.startswith('$test'):
        context = message.content
        non_cmd = context.replace("$test","")
        if "," not in non_cmd:
            await message.channel.send('您输入的指令格式不正确,请重新输入')
            print("User has use command '$test', But format incorrect")
        else:
            args = non_cmd.split(',')  # 检测输入的arguments
            print("User has use command '$test', With arguments: " + str(args))
            if len(args)>=5:
                add_table(time=args[0],holder=args[1],mtID=args[2],members=args[3],end=args[4])
                embed = discord.Embed(title='Meeting-Timetable 会议时刻表', description=str(final_table))
                await message.channel.send(embed=embed)
                print("add table successful,Current Table: \n")
                print(final_table)
            else:
                await message.channel.send("指令缺少所需信息，请检查后重新输入")
                print("errors in arguements, please retype")


client.run('')#这里输入您的机器人ID
