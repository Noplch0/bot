import requests
import json
import time

def getconfig():
    with open(r"botconfig.json",'r',encoding='utf-8')as f:
        config=json.load(f)
    return config

class ItemswithID:
    name=''
    id=0
    def __init__(self,id):
        self.id=id
        config=getconfig()
        r=get_json(url=f'{config["ffxiv"]["data_url"]}Item/{id}',params={})
        self.name=r['Name_chs']
    def info(self):
        print("{'name':%s,'id':%s}"%(self.name,self.id))

class Itemonsale:
    name=""
    id=0
    world=""
    isHQ=False
    retainername=''
    quantity=0
    price=0
    totalprice=0
    def __init__(self,name,id,ishq,seller,world,price,quantity,totalprice):
        self.name=name
        self.id=id
        self.isHQ=ishq
        self.retainername=seller
        self.world=world
        self.price=price
        self.quantity=quantity
        self.totalprice=totalprice
    
    def info(self):
        print("{\n    name:%s,\n    id:%d,\n    HQ:%s,\n    retainername:%s,\n    world:%s,\n    price:%s,\n    quantity:%s,\n    totalprice:%s,\n}"
              %(self.name,self.id,self.isHQ,self.retainername,self.world,self.price,self.quantity,self.totalprice))


def get_json(url,params):
    result=requests.get(url=url,params=params)
    print(url)
    r=json.loads(result.text)
    return r



def get_item_id(name,config):
    data_url=config["ffxiv"]["data_url"]+r"search"
    num=config["ffxiv"]["maxlistnumber"]
    item_params={
        "string":name
    }
    r=get_json(data_url,item_params)
    print(len(r["Results"]))
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


def get_price(item,configs):
    config=getconfig()
    price_url=configs["ffxiv"]["price_url"]+config["ffxiv"]["world"]+'/'+str(item.id)
    params={
        "itemIds":item.id,
        "listings":configs["ffxiv"]["maxcurrentdata"]
    }
    r=get_json(price_url,params=params)
    itemlist=[]
    for i in r["listings"]:
        itemlist.append(
            Itemonsale(
                name=item.name,
                id=item.id,
                ishq=i['hq'],
                seller=i["retainerName"],
                world=i["worldName"],
                price=i["pricePerUnit"],
                quantity=i["quantity"],
                totalprice=i["total"]
            )
        )
    return [itemlist,r["lastUploadTime"]]
    
def timestirp(stamp):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(stamp))