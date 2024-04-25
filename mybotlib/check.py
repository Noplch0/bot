import json5 as json
from ruamel import yaml
from ruamel.yaml.comments import CommentedMap

class BotConfig:
    def read(self,data):
        self.data=self.loader.load(data)
    def __init__(self,filepath='botconfig.yaml') -> None:
        with open(filepath,'r',encoding='utf-8') as f:
            data=f.read()
        self.path=filepath
        self.loader=yaml.YAML(typ='rt')
        self.read(data=data)
    def save(self,path=None):
        with open((self.path if not path else path),'w',encoding='utf-8') as f:
            self.loader.dump(self.data,f)
    def getstring(self):
        with open(self.path,'r',encoding='utf-8') as f:
            return f.read()
    def backup(self):
        with open(self.path+'.backup','w',encoding='utf-8') as f:
            self.loader.dump(self.data,f)
    def delitem(self,index:list):
        def delitembyindex(data:CommentedMap,index:list):
            if len(index)==1:
                data.pop(index[0])
            else:
                delitembyindex(data[index[0]],index[1:])
        delitembyindex(self.data,index)



def notcom(text):
    if len(text)==0:
        return True
    return False if text[0]!=' ' else True

def checksuf(text):
    #print(fr"'{text}',{len(text)}")
    return True if len(text)>0 else False