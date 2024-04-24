from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.model import Group, Friend, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import requests
from graia.ariadne.message.parser.base import DetectPrefix
from graia.broadcast.builtin.decorators import Depend
from graia.broadcast.exceptions import ExecutionStop
from typing import Union
import os
from .img import *
from mybotlib.check import *
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix('蓝p ')):

    config=BotConfig()
    img_path = "saved_image"
    init_img_folder(img_path)
    msg = message.display.split(' ')


    if len(msg[0]) < 1 :
        await app.send_message(sender, "你发的什么几把")
        return
    if pid := msg[0]:
        if not pid.isnumeric():
            await app.send_message(sender, "你发的什么几把")
            return
        result = getpic(pid,config.data)
        if result == -1:
            await app.send_message(sender, '不存在指定图片:(')
        elif result == 1:
            image = Image(path=f'./{img_path}/{pid}.{config.data["pixiv"]["img_format"]}')
            await app.send_message(sender, MessageChain(image))
        else:
            file_list = os.listdir(f'./{img_path}/{pid}')
            img_list = []
            for i in file_list:
                if i.endswith(config.data["pixiv"]["img_format"]):
                    img_list.append(Image(path=f'./{img_path}/{pid}/{i}'))
            else:
                await app.send_message(sender, MessageChain(img_list))
    else:
        await app.send_message(sender, "你发的什么几把")

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix('我要 ')):
    img_path = "saved_image"
    init_img_folder(img_path)
    msg = message.display.split(' ')

    if len(msg[0]) < 1:
        await app.send_message(sender, "你发的什么几把")
        return
    if not os.path.exists(f'{img_path}/{msg[0]}'):
        await app.send_message(sender, '你在想什么不存在的东西')
        return
    await app.send_message(sender, Image(path=f'{img_path}/{msg[1]}'))

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix('来图 ')):

    img_path = "saved_image"
    init_img_folder(img_path)
    msg = message.display.split(' ')

    if len(msg[0]) < 1:
        await app.send_message(sender, "你发的什么几把")
        return
    elif (code:=requests.get(f'{msg[0]}').status_code)!=200:
        await app.send_message(sender,f"{code}!")
    else:
        await app.send_message(sender,MessageChain(Image(url=f'{msg[1]}')))

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix('随机')):
    
    if checksuf(message.display):
        return
    img_path = "saved_image"
    init_img_folder(img_path)

    await app.send_message(sender,MessageChain(Image(path=f'{img_path}/{random_Image()}')))

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix('图片删除 ')):

    img_path = "saved_image"
    init_img_folder(img_path)
    msg = message.display.split(' ')

    if len(msg[0]) < 1:
        await app.send_message(sender, "你发的什么几把")
        return
    failedlist=[]
    for i in msg:
        if del_img(i):
            continue
        else:
            failedlist.append(i)
    await app.send_message(sender,MessageChain(f"{(len(msg)-len(failedlist))} 项删除成功\n{(len(failedlist))} 项删除失败"))

@channel.use(ListenerSchema(listening_events=[ FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix('图片列出')):

    if checksuf(message.display):
        return
    img_path = "saved_image"
    init_img_folder(img_path)
    await app.send_message(sender,str(print_tree(img_path)))

