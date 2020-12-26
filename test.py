import json
from makePreDB import GetData

def getJson():
    with open("timeline/BAO/4819370612.json") as json_file:
        json_data = json.load(json_file)
    return json_data
json_data = getJson()
getData = GetData()
for i in range(0,11):
    print(getData.makeSkillTimeline(json_data, i))