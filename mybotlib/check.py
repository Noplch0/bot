import json
def notcom(text):
    if len(text)==0:
        return True
    return False if text[0]!=' ' else True

def checksuf(text):
    #print(fr"'{text}',{len(text)}")
    return True if len(text)>0 else False
def getconfig():
    with open(r"botconfig.json",'r',encoding='utf-8')as f:
        config=json.load(f)
    return config