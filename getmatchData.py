import pandas as pd
import time
from requests import get
from ConstURL import ConstURL
import json
import os
ConstURL = ConstURL()
apiKey = ConstURL.apiKey
mainUrl = ConstURL.mainUrl

def getMatch(gameId):
    return get(mainUrl + "/lol/match/v4/matches/"+ gameId +"?api_key="+apiKey).json()
    

#match ID is int but getMatch need str data
players = os.listdir("player")
for player in players:
    print(player)
    matchs = pd.read_csv(f"player/{player}", header = 0 , index_col = 0)
    try:
        for matchId in matchs["gameId"].iloc[:3]:
            match = getMatch(str(matchId))
            file_path = f"match/{matchId}.json"
            if os.path.isfile(file_path) == True:
                break
            with open(file_path, 'w') as outfile:
                json.dump(match, outfile, indent = 4)
            time.sleep(1.3)
    except:
        pass




# python3 getmatchData.py