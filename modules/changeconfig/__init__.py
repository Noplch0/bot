from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.model import Group, Friend, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.base import DetectPrefix
from mybotlib.check import *
from .setjson import *

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('查看设置')):

    if checksuf(message.display):
        return
    config=BotConfig()
    if sender.id !=config.data["Admin"]:
            await app.send_message(sender,"啊？")
            return

    mesg=MessageChain(Plain(config.getstring()))
    await app.send_message(sender,mesg)

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('修改设置 ')):

    config=BotConfig()

    if sender.id !=config.data["Admin"]:
            await app.send_message(sender,"啊？")
            return
    
    msg=message.display.split(' ')
    if len(msg)!=2:
        mesg=MessageChain(Plain('参数错误！使用方法例：修改设置 pixiv-fix cat'))
    else:
        index=msg[0].split('-')
        intent=msg[1]
        change_list_intent(config.data,index,intent)
        config.save()
        mesg=MessageChain(["修改成功，现设置为：",Plain(config.getstring())])
    await app.send_message(sender,mesg)
@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('备份设置')):
    if checksuf(message.display):
        return
    config=BotConfig()
    if len(message.display)>=1:
        return

    if sender.id !=config.data["Admin"]:
            mesg='啊？'

    else:
        config.backup()
        mesg=MessageChain(["备份成功，现设置为：",Plain(config.getstring())])
    await app.send_message(sender,mesg)
    
@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def __(app: Ariadne, sender: Friend, message: MessageChain=DetectPrefix('增加设置 ')):
    config=BotConfig()
    msg=message.display.split(' ')
    if sender.id !=config.data["Admin"]:
            mesg='啊？'
    else:
        if len(msg)!=2:
            mesg=MessageChain(Plain('参数错误！使用方法例：增加设置 这个-设置-是 存在的!'))
        else:
            index=msg[0].split('-')
            intent=msg[1]
            add_2_list(config.data,index,intent)
            config.save()
            mesg=MessageChain(["修改成功，现设置为：",
                Plain(config.getstring())
                ]
            )
    await app.send_message(sender,mesg)
