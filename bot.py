import json
import os
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
from typing import Union
if not os.path.exists("botconfig.json"):
    settings={
        "pixiv": {
            "fix": "nl",
            "img_format": "png"
        },
        "Admin": "<your own qq number>",
        "Bot": "<bot qq number>",
        "ffxiv": {
            "data_url": "https://cafemaker.wakingsands.com/",
            "price_url": "https://universalis.app/api/v2/",
            "world": "猫小胖",
            "maxlistnumber": 5,
            "maxcurrentdata": 20
        }
    }
    with open('botconfig.json','w',encoding='utf-8') as f:
        json.dump(settings,f,ensure_ascii=False,sort_keys=True,indent=4)



saya = create(Saya)
with open(r"botconfig.json",'r',encoding='utf-8')as f:
    bot_config=json.load(f)

app = Ariadne(
    connection=config(bot_config['Bot'],"lkijnfgh")
    )


with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            # 假设模组是以 `_` 开头的，就不去导入
            # 根据 Python 标准，这类模组算是私有函数
            continue
        saya.require(f"modules.{module_info.name}")

app.launch_blocking()
