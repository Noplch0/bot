from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import requests
import os
from time import sleep
from typing import Union

channel = Channel.current()


def getpic(pid, geshi='jpg'):
    image_url = f'https://pixiv.nl/{pid}-1.{geshi}'
    print(image_url)
    r = requests.get(image_url)
    if '這個作品可能已被刪除，或無法取得' in r.text:
        return -1
    elif '指定' in r.text:
        image_url = f'https://pixiv.nl/{pid}.{geshi}'
        print(image_url)
        r = requests.get(image_url)
        with open(f'./saved_image/{pid}.{geshi}', 'wb') as f:
            f.write(r.content)
        return 1
    else:
        for i in range(1, 999):
            os.makedirs(f'./saved_image/{pid}', exist_ok=True)
            image_url = f'https://pixiv.nl/{pid}-{i}.{geshi}'
            print(image_url)
            r = requests.get(image_url)
            if '作品' in r.text:
                break
            with open(f'./saved_image/{pid}/{i}.{geshi}', 'wb') as f:
                f.write(r.content)
    return 0


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    path = "saved_image"
    exist = os.listdir('saved_image')
    print(message.display)
    msg = message.display.split(' ')
    if msg[0] == f'蓝p':
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        if pid := message.display.split(' ')[1]:
            fmt = 'png'
            result = getpic(pid, geshi=fmt)
            if result == -1:
                await app.send_message(sender, '没有那种世俗的欲望（404')
            elif result == 1:
                image = element.Image(path=f'./saved_image/{pid}.{fmt}')
                await app.send_message(sender, MessageChain(image))
            elif result == 0:
                file_list = os.listdir(f'./saved_image/{pid}')
                img_list = []
                for i in file_list:
                    if i.endswith(fmt):
                        img_list.append(element.Image(path=f'./saved_image/{pid}/{i}'))
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
        await app.send_message(sender, element.Image(path=f'saved_image/{msg[1]}'))
    if msg[0] == '来图':
        if len(msg) < 2:
            await app.send_message(sender, "你发的什么几把")
            return
        await app.send_message(sender,MessageChain(element.Image(url=f'{msg[1]}')))
