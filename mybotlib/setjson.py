import json5 as json

def format_json(origin_json):
    return json.dumps(origin_json,sort_keys=True,indent=4,ensure_ascii=False)

def saveconfig(config,backup=False):
    with open("%s.json"%('botconfig'if not backup else "botconfig.backup"),'w',encoding='utf-8') as f:
            json.dump(config,f,ensure_ascii=False,indent=4,sort_keys=True)

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
        return str(new)
    elif type(origin)==int:
        return int(new)
    elif type(origin)==bool:
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

def add_2_list(cfg,index:list,indent):
    if len(index)==1:
        cfg[index[0]]=indent
    else:
        add_2_list(cfg[index[0]],index[1:],indent)
    return cfg

