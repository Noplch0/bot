from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from typing import Union
from graia.ariadne.message.parser.base import DetectPrefix
from .utils import genImage
from .xibao import *

from mybotlib.check import *
saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage,FriendMessage]))
async def pornhub_style_logo_generator(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix("5000 ")):
    msg = message.display.split(' ')
    if len(msg) != 2:
        await app.send_message(sender,MessageChain(element.Image(path='./modules/5000zhao/error1.png')))
    elif len(msg)==2:
        left_text, right_text=msg
        try:
            genImage(word_a=left_text, word_b=right_text).save("./modules/5000zhao/test.png")
        except TypeError:
            await app.send_message(sender, MessageChain(element.Image(path="./modules/5000zhao/error.png")))
            return None
        await app.send_message(sender,MessageChain(element.Image(path='./modules/5000zhao/test.png')))


@channel.use(ListenerSchema(listening_events=[GroupMessage,FriendMessage]))
async def pornhub_style_logo_generator(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix("喜报 ")):
    msg = message.display.split(' ')
    if len(msg)<1:
        mesg=MessageChain(element.Image(path='./modules/5000zhao/xibaoerror.jpg'))
    else:
        xibaodotjpg(msg)
        mesg=MessageChain(element.Image(path='./modules/5000zhao/xibao.jpg'))
    await app.send_message(sender,mesg)
    