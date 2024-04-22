from mybotlib.config import *
from fflogsapi import FFLogsClient
from test import *
fapi = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
#print(character.encounter_rankings({"encounterID":1070}))
player=PlayerInf("Storiasd","琥珀原")
print(player.isexist)