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

from .setjson import *

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain):

    config=getconfig()
    head=["修改设置","查看设置",'备份设置','增加设置','删除设置']

    if sender.id !=config["Admin"]:
            await app.send_message(sender,"啊？")
            return
    
    msg=message.display.split(' ')
    if msg[0] not in head:
        return
    if msg[0]==head[1]:
        mesg=MessageChain(
             Plain(
                  format_json(config)
             )
        )
    elif msg[0]==head[0]:
        if len(msg)<=2:
            mesg=MessageChain(Plain('参数错误！使用方法例：修改设置 pixiv-fix cat'))
        else:
            index=msg[1].split('-')
            intent=msg[2]
            change_list_intent(config,index,intent)
            saveconfig(config)
            mesg=MessageChain(["修改成功，现设置为：",
                Plain(
                    format_json(config)
                )
            ]
            )
    elif msg[0]==head[2] and len(msg)==1:
        saveconfig(config,backup=True)
    elif msg[0]==head[3]:
        if len(msg)<=2:
            mesg=MessageChain(Plain('参数错误！使用方法例：增加设置 这个-设置-是 存在的!'))
        else:
            index=msg[1].split('-')
            intent=msg[2]
            add_2_list(config,index,intent)
            saveconfig(config)
            mesg=MessageChain(["修改成功，现设置为：",
                Plain(
                    format_json(config)
                )
            ]
            )
    elif msg[0]==head[4]:
        if len(msg)<=2:
            mesg=MessageChain(Plain('参数错误！使用方法例：删除设置 这个-设置-是不存在的!'))
        else:
            index=msg[1].split('-')
            del_item(config,index)
            mesg=MessageChain(["修改成功，现设置为：",
                Plain(
                    format_json(config)
                )
            ]
            )
