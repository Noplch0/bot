import requests
import json
import time
from mybotlib.check import *

class ItemswithID:
    def __init__(self,id):
        self.id=id
        config=BotConfig()
        r=get_json(url=f'{config.data["ffxiv"]["data_url"]}Item/{id}',params={})
        self.name=r['Name_chs']
    def info(self):
        print("{'name':%s,'id':%s}"%(self.name,self.id))

class Itemonsale:
    def __init__(self,name,id,i,world=BotConfig().data['ffxiv'][ "world"]):
        self.name=name
        self.id=id
        self.isHQ=i['hq']
        self.retainername=i["retainerName"]
        self.price=i["pricePerUnit"]
        self.quantity=i["quantity"]
        self.totalprice=i["total"]
        try:
            self.world=i["worldName"]
        except:
            self.world=world
        self.say=f'({("HQ" if self.isHQ else "NQ")}){self.price}x{self.quantity}(合计{self.totalprice}) {self.retainername}@{self.world}\n'

def get_json(url,params):
    result=requests.get(url=url,params=params)
    r=json.loads(result.text)
    return r



def get_item_id(name,config):
    data_url=config["ffxiv"]["data_url"]+r"search"
    num=config["ffxiv"]["maxlistnumber"]
    item_params={
        "string":name
    }
    r=get_json(data_url,item_params)
    if len(r["Results"])==0:
        return False
    idList=[]
    l=0
    for i in r["Results"]:
        idList.append(ItemswithID(i["ID"]))
        l+=1
        if l >=num:
            break
    return idList[:num]


def get_price(item:ItemswithID,configs,world):
    price_url=configs["ffxiv"]["price_url"]+world+'/'+str(item.id)
    params={
        "itemIds":item.id,
        "listings":configs["ffxiv"]["maxcurrentdata"]
    }
    r=get_json(price_url,params=params)
    itemlist=[]
    for i in r["listings"]:
        item=Itemonsale(name=item.name,id=item.id,i=i)
        itemlist.append(item)
    return [itemlist,r["lastUploadTime"]]
    
def timestirp(stamp):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(stamp))