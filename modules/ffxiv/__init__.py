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
from graia.ariadne.message.parser.base import DetectPrefix
from mylib.check import *

channel = Channel.current()



@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix("查价 ")):
    msg = message.display.split(' ')
    config=getconfig()
    if len(msg)<1:
        chain=MessageChain(Plain("?你想查什么玩意儿？"))
        await app.send_message(sender,chain)
        return
    namelist=get_item_id(msg[0],config)
    if not namelist:
        chain=MessageChain(Plain("这种东西不存在吧"))
        await app.send_message(sender,chain)
        return
    world=msg[-1] if len(msg)>1 else config['ffxiv']['world']
    messagelist=['在 %s 的板子上找到这些数据：\n'%(world)]
    for i in namelist:
        r=get_price(i,config,world)
        if len(r[0])==0:
            continue
        messagelist.append(f"{i.name}:\n")
        for items in r[0]:
            rarestr=f'({"HQ" if items.isHQ else "NQ"}){items.price}x{items.quantity}(合计{items.totalprice}) {items.retainername}@{items.world}\n'
            messagelist.append(rarestr)
        messagelist.append(f"最近更新时间：{timestirp(int(r[1])/1000)}\n")
    chain=MessageChain(messagelist)
    await app.send_message(sender,chain)
