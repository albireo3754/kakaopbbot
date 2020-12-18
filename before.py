import pandas as pd
import os
import json

prodata = pd.read_csv('nickplusID.csv',index_col= 0 ,header=0)

koreanPros = prodata.loc[lambda df: df["country"] == "Korea"]["nickname"]
# print(koreanPros)
# findPro = prodata.nickname == koreanPro
# print(prodata[findPro])
#filtering




def nicknameToSummonername(nickname,prodata):
    findPro = prodata.nickname == nickname
    for summonerName in prodata[findPro]["name"]:
        return summonerName

def findParticipantId(json_data,summonername):
    for pI in json_data["participantIdentities"]:
        # print(kPro)
        if kPro == pI["player"]["summonerName"]:
            # print(participantId)
            return pI["participantId"] 

for koreanPro in koreanPros:
    print(koreanPro)
    kPro = nicknameToSummonername(koreanPro,prodata)

    for jsonURL in os.listdir(f"match/{koreanPro}"):
        with open(f"match/{koreanPro}/{jsonURL}") as json_file:
            json_data = json.load(json_file)

        participantId = findParticipantId(json_data,kPro)
        print(participantId)
        #find participantId

        gameData = json_data["participants"][participantId]
        champion = getchampionName(gameData["championId"])
        spell1Id = getSpellName(gameData["spell1Id"])
        spell2Id = getSpellName(gameData["spell2Id"])
        item = [getItemName(gameData[f"item{i}"]) for i in range(7)]
        break
    break



#pro닉네임땃고, 이제만들어야할게?
#pro닉마다 match 가져와서 계산하기.


# python3 matchInfByPro.py