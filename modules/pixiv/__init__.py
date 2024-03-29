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
import random

channel = Channel.current()

with open('botconfig.json','r') as f:
    config=json.load(f)

def getpic(pid,config):
    fix=config['pixiv']['fix']
    geshi=config['pixiv']["img_format"]
    image_url = f'https://pixiv.{fix}/{pid}-1.{geshi}'
    print(image_url)
    r = requests.get(image_url)
    if '這個作品可能已被刪除，或無法取得' in r.text:
        return -1
    elif '指定' in r.text:
        image_url = f'https://pixiv.{fix}/{pid}.{geshi}'
        print(image_url)
        r = requests.get(image_url)
        os.makedirs(f'./saved_image', exist_ok=True)
        with open(f'./saved_image/{pid}.{geshi}', 'wb') as f:
            f.write(r.content)
        return 1
    else:
        for i in range(1, 999):
            os.makedirs(f'./saved_image/{pid}', exist_ok=True)
            image_url = f'https://pixiv.{fix}/{pid}-{i}.{geshi}'
            print(image_url)
            r = requests.get(image_url)
            if '作品' in r.text:
                break
            with open(f'./saved_image/{pid}/{i}.{geshi}', 'wb') as f:
                f.write(r.content)
    return r.status_code

def random_Image():
    imgList=os.listdir("saved_image")
    img=random.choice(imgList)
    if not img.endswith("png"):
        return random_Image()
    else:
        print(img)
        return img


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    path = "saved_image"
    os.makedirs(f'./saved_image', exist_ok=True)
    exist = os.listdir('saved_image')
    print(message.display)
    msg = message.display.split(' ')
    if msg[0] == f'蓝p':
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        if pid := message.display.split(' ')[1]:
            for i in pid:
                if i not in ['0','1','2','3','4','5','6','7','8','9']:
                    await app.send_message(sender, "你发的什么几把")
                    return
            fmt = 'png'
            result = getpic(pid,config)
            if result == -1:
                await app.send_message(sender, '没有那种世俗的欲望（404')
            elif result == 1:
                image = Image(path=f'./saved_image/{pid}.{fmt}')
                await app.send_message(sender, MessageChain(image))
            else:
                file_list = os.listdir(f'./saved_image/{pid}')
                img_list = []
                for i in file_list:
                    if i.endswith(fmt):
                        img_list.append(Image(path=f'./saved_image/{pid}/{i}'))
                if len(msg) == 3:
                    if msg[2] == '分段':
                        for i in img_list:
                            await app.send_message(sender, MessageChain(i))
                else:
                    await app.send_message(sender, MessageChain(img_list))
        else:
            await app.send_message(sender, "你发的什么几把")
    if msg[0] == '我要':
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        if not os.path.exists(f'saved_image/{msg[1]}'):
            await app.send_message(sender, '你在想什么不存在的东西')
            return
        await app.send_message(sender, Image(path=f'saved_image/{msg[1]}'))
    if msg[0] == '来图':
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        elif (code:=requests.get(f'{msg[1]}').status_code)!=200:
            await app.send_message(sender,f"不对,错了,你要的是{code}")
        else:
            await app.send_message(sender,MessageChain(Image(url=f'{msg[1]}')))
    if msg[0]== '随机':
        await app.send_message(sender,MessageChain(Image(path=f'saved_image/{random_Image()}')))




@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def __(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    msg = message.display.split(' ')
    if msg[0] == '蓝p修改':
        if sender.id !=config["Admin"]:
            await app.send_message(sender,"啊？")
            return
        if len(msg)<=2:
            await app.send_message(sender,"格式错误！使用方法：蓝p修改 <网址后缀/文件后缀> <修改后内容>")
        else:
            if msg[1]=='网址后缀':
                response = f'网址后缀已由{config["pixiv"]["fix"]} 修改为 {msg[2]}'
                config["pixiv"]["fix"]=msg[2]
                with open("./botconfig.json","w") as f:
                    json.dump(config,f)
                await app.send_message(sender,MessageChain(response))
            elif msg[1]=='文件后缀':
                response = f'文件后缀已由{config["pixiv"]["img_format"]} 修改为 {msg[2]}'
                config["pixiv"]["img_format"]=msg[2]
                with open("./botconfig.json","w") as f:
                    json.dump(config,f,ensure_ascii=False,indent=4)
                await app.send_message(sender,MessageChain(response))
    if msg[0]=="备份":
        with open("botconfig.backup.json",'w') as f:
            json.dump(config,f,ensure_ascii=False,indent=4)
        await app.send_message(sender,'哦')
    
    if msg[0]=="看看设置":
        await app.send_message(sender,str(config))
