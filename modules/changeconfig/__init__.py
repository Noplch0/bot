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
from graia.ariadne.message.parser.base import DetectPrefix
from mybotlib.check import *
from .setjson import *

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('查看设置')):

    if checksuf(message.display):
        return
    config=getconfig()

    if sender.id !=config["Admin"]:
            await app.send_message(sender,"啊？")
            return

    mesg=MessageChain(Plain(format_json(config)))
    await app.send_message(sender,mesg)

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('修改设置 ')):

    config=getconfig()

    if sender.id !=config["Admin"]:
            await app.send_message(sender,"啊？")
            return
    
    msg=message.display.split(' ')
    if len(msg)!=2:
        mesg=MessageChain(Plain('参数错误！使用方法例：修改设置 pixiv-fix cat'))
    else:
        index=msg[0].split('-')
        intent=msg[1]
        change_list_intent(config,index,intent)
        saveconfig(config)
        mesg=MessageChain(["修改成功，现设置为：",Plain(format_json(config))])
    await app.send_message(sender,mesg)
@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('备份设置')):
    if checksuf(message.display):
        return
    config=getconfig()
    if len(message.display)>=1:
        return

    if sender.id !=config["Admin"]:
            mesg='啊？'

    else:
        saveconfig(config,backup=True)
        mesg=MessageChain(["备份成功，现设置为：",Plain(format_json(config))])
    await app.send_message(sender,mesg)
    
@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('增加设置 ')):
    config=getconfig()
    msg=message.display.split(' ')
    if sender.id !=config["Admin"]:
            mesg='啊？'
    else:
        if len(msg)!=2:
            mesg=MessageChain(Plain('参数错误！使用方法例：增加设置 这个-设置-是 存在的!'))
        else:
            index=msg[0].split('-')
            intent=msg[1]
            add_2_list(config,index,intent)
            saveconfig(config)
            mesg=MessageChain(["修改成功，现设置为：",
                Plain(
                    format_json(config)
                )
            ]
            )
    await app.send_message(sender,mesg)

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('删除设置 ')):
    config=getconfig()
    msg=message.display.split(' ')
    if sender.id !=config["Admin"]:
            await app.send_message(sender,"啊？")
            return
    else:
        if len(msg)!=2:
            mesg=MessageChain(Plain('参数错误！使用方法例：删除设置 这个-设置-是不存在的!'))
        else:
            index=msg[0].split('-')
            del_item(config,index)
            mesg=MessageChain(["修改成功，现设置为：",
                Plain(
                    format_json(config)
                )
            ]
            )
    await app.send_message(sender,mesg)
