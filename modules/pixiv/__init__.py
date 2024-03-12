from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import requests
import os
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
        with open(f'./savedpic/{pid}.{geshi}', 'wb') as f:
            f.write(r.content)
        return 1
    else:
        for i in range(1, 999):
            os.makedirs(f'./savedpic/{pid}', exist_ok=True)
            image_url = f'https://pixiv.nl/{pid}-{i}.{geshi}'
            print(image_url)
            r = requests.get(image_url)
            if '作品' in r.text:
                break
            with open(f'./savedpic/{pid}/{i}.{geshi}', 'wb') as f:
                f.write(r.content)
    return 0


@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    path = "savedpic"
    print(message.display)
    pid = message.display.split(' ')[1]
    if pid:
        result = getpic(pid, geshi='jpg')
        if result == -1:
            await app.send_message(sender, '没有那种世俗的欲望（404')
        elif result == 1:
            image = element.Image(path=f'./savedpic/{pid}.jpg')
            await app.send_message(sender, MessageChain(image))
        elif result == 0:
            file_list = os.listdir(f'./savedpic/{pid}')
            imglist = []
            for i in file_list:
                imglist.append(element.Image(path=f'./savedpic/{pid}/{i}'))
            await app.send_message(sender, MessageChain(imglist))
