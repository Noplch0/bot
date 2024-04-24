from fflogsapi import FFLogsClient,GQLEnum, FightDifficulty
import fflogsapi
import json
import fflogsapi.data
import requests
from mybotlib.check import *
config=BotConfig()
CLIENT_ID=config.data['ffxiv']["logs"][ "CLIENT_ID"]
CLIENT_SECRET=config.data['ffxiv']["logs"][ "CLIENT_SECRET"]
API_KEY=config.data['ffxiv']["logs"][ "API_KEY"]

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
    elif name in ['p5s']:
        return 83
    elif name in ['p6s']:
        return 84
    elif name in ['p7s']:
        return 85
    elif name in ['p8s门神']:
        return 86
    elif name in ['p8s本体']:
        return 87
    else:
        return False
    
def get_zone_name(id):
    text=requests.get(f"https://cn.fflogs.com/v1/zones?api_key={API_KEY}")
    a=json.loads(text.text)
    for i in a:
        for j in i['encounters']:
            if id==j['id']:
                return j['name']
            
def get_job_name(id):
    jbl=['占','诗','黑魔','黑骑','龙骑','机工','武僧','忍者','骑士','学','召','战','白魔','赤魔','盘','舞','绝枪','镰','贤']
    return jbl[id-1]
      

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
        self.color=colorlist[int(percent)-1]  

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

class Onestage:
    def __init__(self,inf:fflogsapi.data.FFLogsZoneEncounterRanking) -> None:
        self.name=get_zone_name(inf.encounter.id)
        self.logs=LogsColor(inf.rank_percent)
        self.kills=inf.kills
        self.job=get_job_name(inf.best_job.id)
        self.msg=f'{self.name}: {self.logs.color}{self.logs.percent}({self.job}) 过本次数:{self.kills}\n'


def add_enconuterlist(player:PlayerInf):
    zoneidlist=[54,49,44,53,45,43,55,50,42,46]
    zonenamelist={54:'天狱',49:'炼狱',44:"边狱",53:"绝o",45:'绝龙诗',43:'老三绝',55:'极神III',50:'极神II',42:"极神I",46:'幻巧'}
    encounterlist=[]
    msg=''
    for i in zoneidlist:
        rankings=player.client.zone_rankings(filters={
        'metric': GQLEnum('rdps'),
        'zoneID': i,
        'difficulty':(101 if i in [54,49,44] else 100 )
        })
        if len (rankings.encounter_ranks) <1:
            continue
        msg+=f'\n{zonenamelist[i]}:\n'
        for j in rankings.encounter_ranks:
            msg+=Onestage(j).msg
    return msg
        


