#from mybotlib import config
CLIENT_ID="9bd5c9c2-fa60-419a-b943-a2be210c4150"
CLIENT_SECRET="Srnc8CvEJnegzYzYlSV1UeEvbyg5YOs3CEPXUEd9"
API_KEY='3d59e549e758a5057ef923eff9ce0e70'
from fflogsapi import FFLogsClient, GQLEnum, FightDifficulty
import json
import requests
"""fapi = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
character = fapi.get_character({'name':"Storia",'serverSlug':"琥珀原"," serverRegion":"CN"})

print(character.encounter_rankings({"encounterID":1070}))"""

def get_zone_id(name):
    if name in ['p9s','P9S','零式万魔殿 荒天之狱1']:
        return 88
    elif name in ['p10s','P10S','零式万魔殿 荒天之狱2']:
        return 89
    elif name in ['p11s','P11S','零式万魔殿 荒天之狱3']:
        return 90
    elif name in ['p12s门神','P12S门神','门神']:
        return 91
    elif name in ['p12s本体','P12S本体','本体']:
        return 92
    elif name in ['绝亚',"TEA","亚历山大绝境战"]:
        return  1062
    elif name in ['绝神兵','神兵',"UwU","究极神兵绝境战"]:
        return 1061
    elif name in ['巴哈',"UCoB","巴哈姆特绝境战",'绝巴哈']:
        return 1060
    elif name in ['龙诗','龙狮','绝龙诗',"DSR","幻想龙诗绝境战",'dsr',"DSR"]:
        return 1065
    elif name in ['TOP','绝o','绝欧','欧米茄绝境验证战']:
        return 1068
    
def get_zone_name(id):
    text=requests.get(f"https://cn.fflogs.com/v1/zones?api_key={API_KEY}")
    a=json.loads(text.text)
    for i in a:
        for j in i['encounters']:
            if id==j['id']:
                return j['name']
            
def get_job_name(id):
    text=requests.get(f"https://cn.fflogs.com/v1/classes?api_key={API_KEY}")
    a=json.loads(text.text)
    for i in a:
        for j in i["specs"]:
            if id==j['id']:
                return j['name']


class PlayerInf:
    def __init__(self,name,server,region='CN') -> None:
        self.name=name
        self.server=server
        self.region=region
        self.isexist=True
        self.api = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
        try:
            self.client=self.api.get_character({'name':self.name,'serverSlug':self.server," serverRegion":self.region})
        except:
            self.isexist=False

class LogsColor:
    def __init__(self,percent) -> None:
        self.percent=int(percent)
        colorlist=['灰']*25
        colorlist.extend(['绿']*25)
        colorlist.extend(['蓝']*25)
        colorlist.extend(['紫']*20)
        colorlist.extend(['橙']*3)
        colorlist.extend(['粉'])
        colorlist.extend(['金'])
        self.color=colorlist[int(percent)]
    

class PlayerInfInOneStage:
    def __init__(self,player:PlayerInf,encounterID:int):
        self.stagename=get_zone_name(encounterID)
        character=player.client
        inf=character.encounter_rankings({"encounterID":encounterID})
        self.kills=inf.kills
        if self.kills==0:
            return
        self.highest=LogsColor(inf.ranks[0].rank_percent)
        self.avarge=LogsColor(inf.average_performance)
        self.medium=LogsColor(inf.median_performance)
        self.bestjob=get_job_name(inf.ranks[0].best_job.id)



class Allstage:
    def __init__(self,this_player:PlayerInf) -> None:
        self.player=this_player
        self.savage1=PlayerInfInOneStage(this_player,88)
        self.savage2=PlayerInfInOneStage(this_player,89)
        self.savage3=PlayerInfInOneStage(this_player,90)
        self.savage4_front=PlayerInfInOneStage(this_player,91)
        self.savage4_behind=PlayerInfInOneStage(this_player,92)
        self.ucob=PlayerInfInOneStage(this_player,1060)
        self.uwu=PlayerInfInOneStage(this_player,1061)
        self.tea=PlayerInfInOneStage(this_player,1062)
        self.dsr=PlayerInfInOneStage(this_player,1065)
        self.top=PlayerInfInOneStage(this_player,1068)
        self.extreme=PlayerInfInOneStage(this_player,1070)
        
def format_reply(this_result:Allstage):
    mesg=f"查询的{this_result.player.name}@{this_result.player.server}数据如下：\n"
    dicts=this_result.__dict__
    for i in dicts:
        if i=='player':
            continue
        else:
            if dicts[i].kills==0:
                mesg+=f'{dicts[i].stagename}:未过本\n'
                continue
            mesg+=f"{dicts[i].stagename}:{dicts[i].highest.color}{dicts[i].highest.percent}({dicts[i].bestjob}) 过本次数{dicts[i].kills}\n"
    return mesg[:-1]

playera=PlayerInf('Storia','琥珀原')

this_result=PlayerInfInOneStage(playera,get_zone_id('dsr'))
mesg=f"""所查询的玩家\n{this_result.stagename} 数据如下:
击杀次数：{this_result.kills}"""
"""
最高：{this_result.highest.color}{this_result.highest.percent}({this_result.bestjob})
中位数：{this_result.medium.color}{this_result.medium.percent}
平均数：{this_result.avarge.color}{this_result.avarge.percent}"""

print(mesg)