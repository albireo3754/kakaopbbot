from requests import get
import json
itemLink = "http://ddragon.leagueoflegends.com/cdn/10.25.1/data/ko_KR/item.json"
# print(get(itemLink).json())
itemJson = get(itemLink).json()

data = itemJson["data"]
itemDict = {}
for i in data:
    # itemkey = i              1001
    # itemKname = i["name"]  장화

    itemkey = i
    itemKname = data[i]["name"]
    
    itemDict[itemkey] = {"kname":itemKname}

with open("jsonCol/item.json", "w") as outfile:  
    json.dump(itemDict, outfile) 



