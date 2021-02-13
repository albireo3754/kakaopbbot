import pandas as pd
import time
from requests import get
from ConstURL import ConstURL
from base import BASE_DIR
from getInf import getSummonerAccountId
ConstURL = ConstURL()
apiKey = ConstURL.apiKey
mainUrl = ConstURL.mainUrl

def getMatchlists(accountId, endIndex = "30"):
    return get(mainUrl + "/lol/match/v4/matchlists/by-account/"+accountId+"?endIndex="+endIndex+"&api_key=" +apiKey).json()

prodata = pd.read_csv(f'{BASE_DIR}/nickplusID.csv',index_col= 0 ,header=0)



for nickname, name in zip(prodata["nickname"], prodata["name"]):
    try:
        accountId = getSummonerAccountId(name)
        time.sleep(0.02)
        matches = getMatchlists(accountId,"30")['matches']
        matchDf = pd.DataFrame(matches)
        matchDf.to_csv(f"{BASE_DIR}/player/{nickname}.csv", mode='w')
    except Exception as e:
        print(e)
        print(nickname)
        # matchDf = pd.DataFrame()
        # matchDf.to_csv(f"{BASE_DIR}/fail/Fail_{nickname}.csv", mode='w')
        pass
    time.sleep(0.02)


