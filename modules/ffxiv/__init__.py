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
            await app.send_message(sender,chain)
            return
        namelist=get_item_id(msg[1],config)
        if not namelist:
            chain=MessageChain(Plain("这种东西不存在吧"))
            await app.send_message(sender,chain)
            return
        messagelist=['在 %s 的板子上找到这些数据：\n'%(config['ffxiv']['world'])]
        for i in namelist:
            r=get_price(i,config)
            if len(r)==0:
                continue
            messagelist.append(f"{i.name}:\n")
            for items in r:
                rarestr=f'({"HQ" if items.isHQ else "NQ"}){items.price}x{items.quantity}(合计{items.totalprice}) {items.retainername}@{items.world}\n'
                messagelist.append(rarestr)
        chain=MessageChain(messagelist)
        await app.send_message(sender,chain)
