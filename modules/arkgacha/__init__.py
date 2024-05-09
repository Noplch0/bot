from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage,StrangerMessage,TempMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.model import Group, Friend,Stranger,Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from typing import Union
from graia.ariadne.message.parser.base import DetectPrefix
from mybotlib.arkgacha import *


saya = Saya.current()
channel = Channel.current()
functionlist= ['抽卡记录']

@channel.use(ListenerSchema(listening_events=[FriendMessage,StrangerMessage,TempMessage]))
async def _(app: Ariadne, sender: Union[Friend,Member,Stranger], message: MessageChain=DetectPrefix("粥 ")):
    
    private_funcrtionlist=functionlist
    private_funcrtionlist.append('登录')
    print(sender,sender.__dict__)
    print(message.__dict__)
    data=HyperGryphAccount()
    msg = message.display.split(' ')
    if msg[0] not in private_funcrtionlist:
        mesg='唉，皱皮'
    match msg[0]:
        case '抽卡记录':
            mesg=data.get_gacha_history(sender=str(sender.id))
        case "登录":
            s=data.add_token(phone=msg[1],pwd=msg[2],sender=sender.id)
            if not s:
                mesg='登录大概是失败了'
            else:
                mesg='登录大概是成功了'
                data.save_token()

    await app.send_message(sender,mesg)

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def _(app: Ariadne, sender: Group, message: MessageChain=DetectPrefix("粥 ")):
    print(sender,sender.__dict__)
    print(message.__dict__)
    data=HyperGryphAccount()
    msg = message.display.split(' ')
    if msg[0] not in functionlist:
        mesg='唉，皱皮'
    match msg[0]:
        case '抽卡记录':
            mesg=data.get_gacha_history(sender=str(sender.id))
    await app.send_message(sender,mesg)