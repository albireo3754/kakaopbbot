from requests import get
import json
spellLink = "http://ddragon.leagueoflegends.com/cdn/10.25.1/data/ko_KR/summoner.json"
# print(get(spellLink).json())
spellJson = get(spellLink).json()

data = spellJson["data"]
spellDict = {}
for i in data:
    # spellkey = data[i]["key"]       4
    # spellEname = i                 summonerFlash
    # spellKname = data[i]["name"] 방어막

    spellkey = data[i]["key"]
    spellEname = i
    spellKname = data[i]["name"]
    
    spellDict[spellkey] = {"ename":i, "kname":spellKname}

with open("jsonCol/spell.json", "w") as outfile:  
    json.dump(spellDict, outfile) 



