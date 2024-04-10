import json
import distutils
def format_json(origin_json):
    return json.dumps(origin_json,sort_keys=True,indent=4)

def getconfig():
    with open(r"botconfig.json",'r',encoding='utf-8')as f:
        config=json.load(f)
    return config

def saveconfig(config,backup=False):
    with open("%s.json"%('botconfig'if not backup else "botconfig.backup"),'w',encoding='utf-8') as f:
            json.dump(config,f,ensure_ascii=False,indent=4)

def change_list_intent(list,namelist,newintent=False):
    a=list
    for i in namelist[:-1]:
        try:
            a=a[i]
        except:
            return False
    if newintent:
        a[namelist[-1]]=change_type(a[namelist[-1]],newintent)

def change_type(origin,new):
    if type(origin)==type(new):
        return new
    elif type(origin)==str:
        print('changed to str')
        return str(new)
    elif type(origin)==int:
        print('changed to int')
        return int(new)
    elif type(origin)==bool:
        print('changed to bbool')
        if new=="True":
            return True
        if new=="False":
            return False


def construct_dict(index:list,indent):
    a={}
    if len(index)==1:
        a.update({index[0]:indent})
    else:
        a.update({index[0]:construct_dict(index[1:],indent)})
    return a

def add_2_list(list:dict,index:list,indent):
    list.update(construct_dict(index,indent))
    return list

def del_item(dic:dict,index:list):
    if len(index)==1:
        dic.pop(index[0])
    else:
        del_item(dic[index[0]],index[1:])

