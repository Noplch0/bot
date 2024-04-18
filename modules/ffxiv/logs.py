"""import json
import requests
import pandas as pd
from fflogsapi import FFLogsClient
def getconfig():
    with open(r"botconfig.json",'r',encoding='utf-8')as f:
        configs=json.load(f)
    return configs
client = FFLogsClient("9bd5c9c2-fa60-419a-b943-a2be210c4150", "Srnc8CvEJnegzYzYlSV1UeEvbyg5YOs3CEPXUEd9")
def chachengfen(id,server):
    configs=getconfig()
    client = FFLogsClient("9bd5c9c2-fa60-419a-b943-a2be210c4150", "Srnc8CvEJnegzYzYlSV1UeEvbyg5YOs3CEPXUEd9")
    client.rate_limit_spent()
chachengfen('Storia','琥珀原')"""

CLIENT_ID="9bd5c9c2-fa60-419a-b943-a2be210c4150"
CLIENT_SECRET="Srnc8CvEJnegzYzYlSV1UeEvbyg5YOs3CEPXUEd9"
from fflogsapi import FFLogsClient, GQLEnum, FightDifficulty
fapi = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
character = fapi.get_character({'name':"Storia",'serverSlug':"琥珀原"," serverRegion":"CN"})
abyssos = fapi.get_zone(id=43)

print(character.encounter_rankings({"encounterID":1062}))