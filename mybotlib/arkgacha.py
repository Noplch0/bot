import requests
import json5 as json
from mybotlib.setjson import *
from time import sleep

def get_token_by_password(phone,pwd):
    data={'phone':phone,
          'password':pwd}
    response=requests.post(url='https://as.hypergryph.com/user/auth/v1/token_by_phone_password',
                           json=data)
    
    if '失败' in response.content:
        return False
    return json.loads(response.content)['data']['token']


class SixStarRecord:
    def __init__(self,name) -> None:
        self.name=name
        self.amount=1
    def add(self):
        self.amount+=1
        
class PoolRecord:
    
    def __init__(self,poolname) -> None:
        self.records=[0,0,0,0,0,0]
        self.six_stars={}
        self.total=0
        self.name=poolname
    def add_record(self,record:list):
        for i in record:
            self.total+=1
            self.records[i["rarity"]]+=1
            if i["rarity"]==5:
                if i['name'] in self.six_stars.keys():
                    self.six_stars[i['name']]+=1
                else:
                    self.six_stars.update({i['name']:1})
            else:
                continue
    def inf(self):
        result=f'\n{self.name}:\n总抽数：{self.total}\n'
        print(self.six_stars)
        print(len(self.six_stars))
        for i in self.six_stars:
            result+=f'{i}:{self.six_stars[i]}\n'
        result+=f"五星：{self.records[4]}\n四星：{self.records[3]}\n三星：{self.records[2]}\n"
        return result

        
class HyperGryphAccount:
    def read(self):
        with open('./mybotlib/utils/arktoken.json','r',encoding='utf-8') as f:
            self.data=json.load(f,encoding='utf-8')
    def add_by_token(self,sender,token):
        add_2_list(self.data,[sender],token)
        self.save_token()

    def get_gacha_history(self,sender):
        i=0
        gachalist=[]
        if sender not in self.data.keys():
            return '请先登录(登录请私聊以免暴露信息，登陆方式：粥 登录 账号 密码)'
        token=self.data[sender]
        while True:
            i+=1
            data={
                'token':token,
                'channelId':1,
                'page':i
                }
            response=requests.get(url='https://ak.hypergryph.com/user/api/inquiry/gacha',
                                  params=data)
            results=read_str(response.content)
            if results['code']==3000:
                return "登陆凭证过期，请重新登录（登录请私聊以免暴露信息,登陆方式：粥 登录 账号 密码）"
            if not len(results['data']['list'])>=1:
                break
            else:
                gachalist+=results['data']['list']
        return self._str(sender=sender,gachalist=gachalist)
        

    def __init__(self):
        self.read()

    def add_token(self,phone,pwd,sender) -> None:
        token=get_token_by_password(phone,pwd)
        add_2_list(self.data,[sender],token)

    def _str(self,sender,gachalist):
        oldname=''
        record=''
        result=f'抽卡记录如下：\n'
        for i in gachalist:
            newname=i['pool']
            if newname!=oldname:
                if record!='':
                    result+=record.inf()
                record=PoolRecord(newname)
                record.add_record(i['chars'])
                oldname=newname
            elif newname==oldname:
                record.add_record(i['chars'])
        return result[:-1]
            
    def save_token(self):
        with open('./mybotlib/utils/arktoken.json','w',encoding='utf-8') as f:
            json.dump(self.data,f,ensure_ascii=False,indent=4,sort_keys=True)