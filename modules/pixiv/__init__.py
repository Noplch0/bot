from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.model import Group, Friend, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import requests
from graia.broadcast.builtin.decorators import Depend
from graia.broadcast.exceptions import ExecutionStop
from typing import Union
import os
import json
from .img import *

channel = Channel.current()

def getconfig():
    with open(r"botconfig.json",'r',encoding='utf-8')as f:
        config=json.load(f)
    return config


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):

    config=getconfig()
    img_path = "saved_image"
    init_img_folder(img_path)

    print(message.display)
    msg = message.display.split(' ')


    if msg[0] == '蓝p':
        if len(msg) < 2 :
            await app.send_message(sender, "你发的什么几把")
            return
        if pid := msg[1]:
            if not pid.isnumeric():
                await app.send_message(sender, "你发的什么几把")
                return
            result = getpic(pid,config)
            if result == -1:
                await app.send_message(sender, '不存在指定图片:(')
            elif result == 1:
                image = Image(path=f'./{img_path}/{pid}.{config["pixiv"]["img_format"]}')
                await app.send_message(sender, MessageChain(image))
            else:
                file_list = os.listdir(f'./{img_path}/{pid}')
                img_list = []
                for i in file_list:
                    if i.endswith(config["pixiv"]["img_format"]):
                        img_list.append(Image(path=f'./{img_path}/{pid}/{i}'))
                else:
                    await app.send_message(sender, MessageChain(img_list))
        else:
            await app.send_message(sender, "你发的什么几把")


    if msg[0] == '我要':
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        if not os.path.exists(f'{img_path}/{msg[1]}'):
            await app.send_message(sender, '你在想什么不存在的东西')
            return
        await app.send_message(sender, Image(path=f'{img_path}/{msg[1]}'))


    if msg[0] == '来图':
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        elif (code:=requests.get(f'{msg[1]}').status_code)!=200:
            await app.send_message(sender,f"不对,错了,你要的是{code}")
        else:
            await app.send_message(sender,MessageChain(Image(url=f'{msg[1]}')))


    if msg[0]== '随机':
        await app.send_message(sender,MessageChain(Image(path=f'{img_path}/{random_Image()}')))


    if msg[0] == "图片删除":
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        if del_img(msg[1]):
            await app.send_message(sender,str(print_tree(img_path))+'删除成功')
        else:
            await app.send_message(sender,str(print_tree(img_path))+'删除失败')

    if msg[0]=='图片列出':
        await app.send_message(sender,str(print_tree(img_path)))

