from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image,Plain
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from typing import Union

from .utils import genImage
from .xibao import *

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage,FriendMessage]))
async def pornhub_style_logo_generator(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    msg = message.display.split(' ')
    if msg[0] == '5000' and len(msg) != 3:
        await app.send_message(sender,MessageChain(Image(path='./modules/5000zhao/error1.png')))
    elif msg[0]=='5000' and len(msg)==3:
        _, left_text, right_text=msg
        try:
            genImage(word_a=left_text, word_b=right_text).save("./modules/5000zhao/test.png")
        except TypeError:
            await app.send_message(sender, MessageChain(Image(path="./modules/5000zhao/error.png")))
            return None
        await app.send_message(sender,MessageChain(Image(path='./modules/5000zhao/test.png')))
    elif msg[0]=='喜报':
        if len(msg)<2:
            msg=MessageChain(Image(path='./modules/5000zhao/xibaoerror.jpg'))
        else:
            xibaodotjpg(msg[1:])
            msg=MessageChain(Image(path='./modules/5000zhao/xibao.jpg'))
        await app.send_message(sender,msg)
    