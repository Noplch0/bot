from nonebot import on_command
from nonebot.adapters.qq import Message, MessageSegment, MessageEvent
from nonebot.params import CommandArg
import requests
import os

pixiv = on_command("蓝p", aliases={"pixiv", "pid"})


def getpic(pid, geshi='jpg'):
    image_url = f'https://pixiv.nl/{pid}-1.{geshi}'
    r = requests.get(image_url)
    if '這個作品可能已被刪除，或無法取得' in r.text:
        return -1
    elif '個作品ID中有只有一張圖片，不需要指定是第幾張圖' in r.text:
        image_url = f'https://pixiv.nl/{pid}.{geshi}'
        r = requests.get(image_url)
        with open(f'./savedpic/{pid}.{geshi}', 'wb') as f:
            f.write(r.content)
        return 1
    else:
        for i in range(1, 999):
            os.makedirs(f'./savedpic/{pid}', exist_ok=True)
            image_url = f'https://pixiv.nl/{pid}-{i}.{geshi}'
            r = requests.get(image_url)

            if '作品' in r.text:
                break

            with open(f'./savedpic/{pid}/{i}.{geshi}', 'wb') as f:
                f.write(r.content)
    return 0


@pixiv.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    path = "savedpic"
    if pid := args.extract_plain_text():
        result = getpic(pid, geshi='jpg')
        if result == -1:
            await pixiv.send('没有那种世俗的欲望（404')
        elif result == 1:
            image = MessageSegment.file_image(f'./savedpic/{pid}.jpg')
            await pixiv.send(image)
        elif result == 0:
            file_list = os.listdir(f'./savedpic/{pid}')
            imglist = []
            for i in file_list:
                image = MessageSegment.file_image(f'./savedpic/{pid}/{i}')
                await pixiv.send(image)
