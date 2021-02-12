import pandas as pd
import time
from requests import get
from ConstURL import ConstURL
import json
import os
from base import BASE_DIR
ConstURL = ConstURL()
apiKey = ConstURL.apiKey
mainUrl = ConstURL.mainUrl

def getMatch(gameId):
    return get(mainUrl + "/lol/match/v4/matches/"+ gameId +"?api_key="+apiKey).json()
    
def getTimeLine(matchId):
    return get(mainUrl + "/lol/match/v4/timelines/by-match/"+ matchId +"?api_key="+apiKey).json()

#match ID is int but getMatch need str data
players = os.listdir("player")
if not os.path.isdir(f'{BASE_DIR}/match'):
    os.mkdir(f'{BASE_DIR}/match')

if not os.path.isdir(f'{BASE_DIR}/timeline'):
    os.mkdir(f'{BASE_DIR}/timeline')
for player in players:
    print(player)
    matchs = pd.read_csv(f"{BASE_DIR}/player/{player}", header = 0 , index_col = 0)
    
    try:
        for matchId in matchs["gameId"].iloc[16:30]:
            if matchId<4803000000:
                #480300000 이전 data들은 10.23패치라 쓸모없음
                continue

            file_path_match = f"{BASE_DIR}/match/{player[:-4]}/{matchId}.json"
            path = f"{BASE_DIR}/match/{player[:-4]}"
            #이미 만들어논건 만들필요가 X
            if not os.path.isdir(path):
                os.mkdir(path)
            if os.path.isfile(file_path_match) == False:
                match = getMatch(str(matchId))
                if "status" in match:
                    continue
                time.sleep(0.02)

            
            
            
            file_path_timeline = f"{BASE_DIR}/timeline/{player[:-4]}/{matchId}.json"
            path = f"{BASE_DIR}/timeline/{player[:-4]}"
            if not os.path.isdir(path):
                os.mkdir(path)
            if os.path.isfile(file_path_timeline) == False:
                timeline = getTimeLine(str(matchId))
                if "status" in timeline:
                    continue
                with open(file_path_match, 'w') as outfile:
                    json.dump(match, outfile, indent = 4)
                with open(file_path_timeline, 'w') as outfile:
                    json.dump(timeline, outfile, indent = 4)
                print(matchId)
                time.sleep(0.02)
            
    except Exception as e:
        print(e)




# python3 getmatchData.py