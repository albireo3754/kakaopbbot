
# http://ddragon.leagueoflegends.com/cdn/10.24.1/data/ko_KR/runesReforged.json rune
# https://raw.communitydragon.org/10.24/game/assets/perks/styles/ link
mainUrl = "https://kr.api.riotgames.com"
apiKey = "RGAPI-4858451d-c548-4ea0-8624-9c15c9124a77"
prodata = pd.read_csv('MyDrive/filename.csv',index_col= 0 ,header=0)
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
newpd = pd.DataFrame(columns = {"name", "accountId", "id", "puuid"})

for i in prodata.loc[:,"id"]:
    time.sleep(1.3)
    sumDict = getSummonerInf(i)
    print(i)
    for k in ["profileIconId", "revisionDate", "summonerLevel"]:
        try:
            sumDict.pop(k)
        except:
            pass
    try:
        newpd = newpd.append(sumDict, ignore_index=True)
    except:
        pass
# 씨발
newpd.to_csv("MyDrive/filename5.csv", mode="w")

# FakerAccId = getSummonerAccountId("Hide On Bush")
# #https://developer.riotgames.com/apis#match-v4/GET_getMatch
# FakerRecentGameId = getGameId(FakerAccId, 0)
# #"id" Encrypted summoner ID, "accountId" is Encrypted account ID,
# # Encrypted PUUID "puuid", "name = miki"
# # print(getMatchInf(miki["accountId"])['matches'][0])
# FakerMatch = getMatch(FakerRecentGameId)


def renameProdata(prodata):
    prodata.rename(columns={"name":'nickname', "id": "name"}, inplace = True)

def teamNameChange():
    prodata.replace({'team': np.nan}, {'team': 'No Team'},inplace=True)

def prodataPackage():
    prodata = pd.read_csv('MyDrive/filename.csv',index_col= 0 ,header=0)
    # renameProdata(prodata)
    # teamNameChange()
    # prodata.to_csv("MyDrive/filename.csv", mode="w")
    return prodata
# prodata= prodataPackage()
def newPd():
    return pd.read_csv('MyDrive/filename5.csv',index_col= 0 ,header=0)
def dropStatus():
    print(newpd.drop("status", axis =1, inplace=True))

def removeNoiseName():
    prodata.loc[:,"name"] = prodata.loc[:,"name"].lstrip()

prodata = pd.read_csv("MyDrive/nickplusID.csv",index_col=0, header=0)
def mergeDataNickname(data,newdata):
    a = pd.merge(prodata.astype(str), newpd.astype(str), how= "outer", left_on = "name", right_on = "name")
    a.to_csv("MyDrive/filename6.csv", mode="w")

# prodata["name"] = [i.lstrip() for i in prodata["name"]]

# prodata.dropna(inplace=True)

# mergeDataNickname(prodata,newpd)



# print(newpd.head())
