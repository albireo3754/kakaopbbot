import pandas as pd
import time
from requests import get
from ConstURL import ConstURL

ConstURL = ConstURL()
apiKey = ConstURL.apiKey
mainUrl = ConstURL.mainUrl

def getMatchlists(accountId, endIndex = "30"):
    return get(mainUrl + "/lol/match/v4/matchlists/by-account/"+accountId+"?endIndex="+endIndex+"&api_key=" +apiKey).json()

prodata = pd.read_csv('nickplusID.csv',index_col= 0 ,header=0)



for nickname, accountId in zip(prodata["nickname"], prodata["accountId"]):
    try:
        matches = getMatchlists(accountId,"30")['matches']
        matchDf = pd.DataFrame(matches)
        matchDf.to_csv(f"player/{nickname}.csv", mode='w')
    except:
        matchDf = pd.DataFrame()
        matchDf.to_csv(f"fail/Fail_{nickname}.csv", mode='w')
        pass
    time.sleep(1.3)


