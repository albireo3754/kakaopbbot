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
        for matchId in matchs["gameId"].iloc[7:12]:
            match = getMatch(str(matchId))
            
            if matchId<4803000000:
                #480300000 이전 data들은 10.23패치라 쓸모없음
                break
            print(matchId)
            file_path = f"match/{matchId}.json"
            #이미 만들어논건 만들필요가 X
            if os.path.isfile(file_path) == True:
                break
            with open(file_path, 'w') as outfile:
                json.dump(match, outfile, indent = 4)
            time.sleep(1.3)
    except KeyboardInterrupt:
        pass




# python3 getmatchData.py