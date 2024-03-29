
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

# 插件信息
__name__ = "5000ZhaoStyleImageGenerator"
__description__ = "一个 5000兆円欲しい! style的图片生成器"
__author__ = "SAGIRI-kawaii"
__usage__ = "发送 `5000兆 text1 text2` 即可"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


@channel.use(ListenerSchema(listening_events=[GroupMessage,FriendMessage]))
async def pornhub_style_logo_generator(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    msg = message.display.split(' ')
    if msg[0] == '5000' and len(msg) != 3:
        await app.send_message(sender,MessageChain(Image(path='./modules/5000zhao/error.png')))
    if msg[0]=='5000' and len(msg)==3:
        _, left_text, right_text=msg
        try:
            genImage(word_a=left_text, word_b=right_text).save("./modules/5000zhao/test.png")
        except TypeError:
            await app.send_message(sender, MessageChain(Image(path="./modules/5000zhao/error.png")))
            return None
        await app.send_message(sender,MessageChain(Image(path='./modules/5000zhao/test.png')))
    