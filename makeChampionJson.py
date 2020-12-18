from requests import get
import json
championLink = "http://ddragon.leagueoflegends.com/cdn/10.24.1/data/ko_KR/champion.json"
# print(get(championLink).json())
championJson = get(championLink).json()

data = championJson["data"]
chamDict = {}
for i in data:
    # chamkey = data[i]["key"]       233
    # chamEname = i                 Aatrox
    # chamKname = data[i]["name"] 아트록스

    chamkey = data[i]["key"]
    chamEname = i
    chamKname = data[i]["name"]
    
    chamDict[chamkey] = {"chamEname":i, "chamKname":chamKname}

with open("champion.json", "w") as outfile:  
    json.dump(chamDict, outfile) 



