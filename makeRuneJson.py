from requests import get
import json
runeLink = "http://ddragon.leagueoflegends.com/cdn/10.24.1/data/ko_KR/runesReforged.json"
# print(get(runeLink).json())
runeJson = get(runeLink).json()

data = runeJson
runeDict = {}
for i in data:
    # runekey = data[i]["id"]       233 champion이랑은 다름
    # runeEname = data[i]["key"]                 Aatrox
    # runeKname = data[i]["name"] 아트록스

    runekey = i["id"]
    runeEname = i["key"]
    runeKname = i["name"]

    runeDict[runekey] = {"ename":runeEname, "kname":runeKname}
    for j in i["slots"]:
        for k in j["runes"]:
            runekey = k["id"]
            runeEname = k["key"]
            runeKname = k["name"]       
            print(runeKname)
            runeDict[runekey] = {"ename":runeEname, "kname":runeKname}
with open("jsonCol/rune.json", "w") as outfile:  
    json.dump(runeDict, outfile) 



