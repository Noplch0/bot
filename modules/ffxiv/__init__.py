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
from .universails import *

channel = Channel.current()

with open(r"botconfig.json",'r',encoding='utf-8')as f:
    config=json.load(f)

@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    msg = message.display.split(' ')
    if msg[0]=='查价':
        if len(msg)<2:
            chain=MessageChain(Plain("?你想查什么玩意儿？"))
            return
        namelist=get_item_id(msg[1],config)
        if not namelist:
            chain=MessageChain(Plain("这种东西不存在吧"))
            return
        messagelist=[f'在 {config['ffxiv']['world']} 的板子上找到这些数据：\n']
        for i in namelist:
            messagelist.append(f"{i.name}:\n")
            r=get_price(i,config)
            rarestr=f'({"HQ" if r.isHQ else "NQ"}){r.price}x{r.quantity}(合计{r.totalprice}) {r.retainername}@{r.world}'
            messagelist.append(rarestr)
        chain=MessageChain(messagelist)


    await app.send_message(sender,chain)