from graia.ariadne.app import Ariadne
import pkgutil
from graia.ariadne.entry import config
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Saya
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
import requests
import os

saya=create(Saya)

app = Ariadne(
    config(
        verify_key="lkijnfgh",  # 填入 VerifyKey
        account=3079809050,  # 你的机器人的 qq 号
        # 以下两行（不含注释）里的 host 参数的地址
        # 是你的 mirai-api-http 地址中的地址与端口
        # 他们默认为 "http://localhost:8080"
        # 如果你 mirai-api-http 的地址与端口也是 localhost:8080
        # 就可以删掉这两行，否则需要修改为 mirai-api-http 的地址与端口
        #HttpClientConfig(host="localhost:8080"),
        #WebsocketClientConfig(host="localhost:8080"),
    ),
)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            # 假设模组是以 `_` 开头的，就不去导入
            # 根据 Python 标准，这类模组算是私有函数
            continue
        saya.require(f"modules.{module_info.name}")


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
    path = "./savedpic"
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

app.launch_blocking()
