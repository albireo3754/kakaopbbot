from requests import get
import json
# http://ddragon.leagueoflegends.com/cdn/10.24.1/data/ko_KR/runesReforged.json rune
# https://raw.communitydragon.org/10.24/game/assets/perks/styles/ link
mainUrl = "https://kr.api.riotgames.com"
apiKey = "RGAPI-c3acb177-4ff3-4aaf-a134-3bba00424a22"

def getSummonerInf(summonerName):
    return get(mainUrl + "/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" +  apiKey).json()

def getSummonerAccountId(summonerName):
    return getSummonerInf(summonerName)["accountId"]

#무조건 str로 넣어야함
def getMatchlists(accountId, endIndex = "10"):
    return get(mainUrl + "/lol/match/v4/matchlists/by-account/"+accountId+"?endIndex="+endIndex+"&api_key=" +apiKey).json()

def getMatch(gameId):
    return get(mainUrl + "/lol/match/v4/matches/"+ gameId +"?api_key="+apiKey).json()
    
def printJson(jsonData):
    print(json.dumps(jsonData, indent="\t") )

def getGameId(accountId, cnt = 0):
    return str(getMatchlists(accountId)['matches'][0]['gameId'])

for i in lists:
    sumDict = getSummonerInf(i)
    for k in ["profileIconId", "revisionDate", "summonerLevel"]:
        try:
            sumDict.pop(k)
        except:
            continue
    if len(sumDict) > 2:
        
    



# FakerAccId = getSummonerAccountId("Hide On Bush")
# #https://developer.riotgames.com/apis#match-v4/GET_getMatch
# FakerRecentGameId = getGameId(FakerAccId, 0)
# #"id" Encrypted summoner ID, "accountId" is Encrypted account ID,
# # Encrypted PUUID "puuid", "name = miki"
# # print(getMatchInf(miki["accountId"])['matches'][0])
# FakerMatch = getMatch(FakerRecentGameId)