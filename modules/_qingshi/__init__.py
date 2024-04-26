from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message import element
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from typing import Union
import random

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    msg = message.display.split(' ')
    sb=0
    jiao=['笑杯','圣杯','阴杯']
    if msg[0]=='关圣帝君':
        i=random.randint(0,10000)
        if i ==9999:
            await app.send_message(sender,'当天我给你9999个巴掌')
        else:
            if len(msg)!=1:
                if int(msg[1])<=0:
                    await app.send_message(sender,f'当天我给你{0-int(msg[1])}个巴掌')
                
                elif int(msg[1])>1:
                    for j in range(0,int(msg[1])):
                        result=random.randint(0,1)+random.randint(0,1)
                        if result==1:
                            sb+=1
                    await app.send_message(sender,f'您获得了{sb}个圣杯')
            else :
                    result=random.randint(0,1)+random.randint(0,1)
                    await app.send_message(sender,f'{jiao[result]},{result}')   