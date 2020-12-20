import pandas as pd
import os
import json


prodata = pd.read_csv('orrn.csv', encoding="cp949")


data = prodata["key"]
prodata = prodata.set_index("key")
print(prodata.head())
itemDict = {}
for i in data:
    # itemkey = i              1001
    # itemKname = i["name"]  장화

    itemkey = str(i)
    itemEname = prodata["ename"][i]
    print(itemEname)
    itemBefore = prodata.loc[i]["before"]
    print(itemBefore)
    
    itemDict[itemkey] = {"ename":itemEname, "before":str(itemBefore)}

with open("jsonCol/orrnItem.json", "w") as outfile:  
    json.dump(itemDict, outfile) 