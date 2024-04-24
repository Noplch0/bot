from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.model import Group, Friend, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from typing import Union
from .universails import *
from .logs import *
from graia.ariadne.message.parser.base import DetectPrefix
from mybotlib.check import *

channel = Channel.current()



@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix("查价 ")):
    msg = message.display.split(' ')
    config=BotConfig()
    if len(msg)<1:
        mesg=MessageChain(Plain("?你想查什么玩意儿？"))
        await app.send_message(sender,mesg)
        return
    namelist=get_item_id(msg[0],config.data)
    if not namelist:
        mesg=MessageChain(Plain("这种东西不存在吧"))
        await app.send_message(sender,mesg)
        return
    world=msg[-1] if len(msg)>1 else config.data['ffxiv']['world']
    mesg='在 %s 的板子上找到这些数据：\n'%(world)
    for i in namelist:
        mesg+='\n'
        r=get_price(i,config.data,world)
        if len(r[0])==0:
            continue
        mesg+=f"{i.name}:\n"
        for items in r[0]:
            mesg+=items.say
        mesg+=f"最近更新时间：{timestirp(int(r[1])/1000)}\n"
    await app.send_message(sender,mesg[:-1])



@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix("查logs ")):
    msg = message.display.split(' ')
    await app.send_message(sender,f'正在查{msg[0]}的橙粉')
    if len(msg)<1:
        mesg=MessageChain(Plain("?你想查什么玩意儿？"))
    elif len(msg)==1:
        name,server=msg[0].split('@')
        player=PlayerInf(name,server)
        if player.client.hidden():
            mesg="该玩家已隐藏logs"
        elif not player.isexist:
            mesg="查询玩家不存在！"
        else:
            mesg=f"""所查询的玩家{name}@{server}数据如下:\n"""
            mesg+=add_enconuterlist(player)
        
    elif len(msg)==2:
        name,server=msg[0].split('@')
        player=PlayerInf(name,server)
        if not player.isexist:
            mesg="查询玩家不存在！"
        else:
            zonename=get_zone_id(msg[1])
            if zonename==False:
                mesg='查询副本不存在!'
            else:
                this_result=PlayerInfInOneStage(player,get_zone_id(msg[1]))
                mesg=f"""所查询的玩家{name}@{server}\n在{this_result.stagename}中数据如下:\n"""
                if this_result.kills==0:
                    mesg+='未过本'
                else:
                    mesg+=f"""击杀次数：{this_result.kills}\n最高：{this_result.highest.color}{this_result.highest.percent}({this_result.bestjob})\n中位数：{this_result.medium.color}{this_result.medium.percent}\n平均数：{this_result.avarge.color}{this_result.avarge.percent}\n"""
    await app.send_message(sender,mesg[:-1])


#因为群里有个傻逼一直叫所以加了这个
@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def _(app: Ariadne, sender: Union[Group, Friend], message: MessageChain=DetectPrefix("查户籍 ")):
    await app.send_message(sender,'你查你妈呢')