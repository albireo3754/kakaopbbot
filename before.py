import pandas as pd
import os
import json
from pymongo import MongoClient
client = MongoClient()

pro = client["pro"]
champion = client["champion"]
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

def findParticipantId(json_data,summonerName):
    for pI in json_data["participantIdentities"]:
        # print(kPro)
        if summonerName == pI["player"]["summonerName"]:
            # print(participantId)
            return pI["participantId"] 

class DataDragon:

    def __init__(self):
        self.champion = self.getChampionData()
        self.spell = self.getSpellData()
        self.item = self.getItemData()
        self.rune = self.getRuneData()

    def getChampionData(self):
        with open("jsonCol/champion.json") as json_file:
            json_data = json.load(json_file)
        return json_data

    def getSpellData(self):
        with open("jsonCol/spell.json") as json_file:
            json_data = json.load(json_file)
        return json_data

    def getItemData(self):
        with open("jsonCol/item.json") as json_file:
            json_data = json.load(json_file)
        return json_data
    
    def getRuneData(self):
        with open("jsonCol/rune.json") as json_file:
            json_data = json.load(json_file)
        return json_data

class GetData(DataDragon):
    
    #get key by int (3) return kname like "갈리오"
    def getChampionName(self, key):
        return self.champion[str(key)]["kname"]

    def getSpellName(self, key):
        return self.spell[str(key)]["kname"]

    def getItemName(self, key):
        if key == 0:
            return None
        return self.item[str(key)]["kname"]

    def getRuneName(self, key):
        return self.rune[str(key)]["kname"]


def test():
    data = GetData()
    for koreanPro in koreanPros:
        # print(koreanPro)
        #Keria
        kPro = nicknameToSummonername(koreanPro,prodata)

        for jsonURL in os.listdir(f"match/{koreanPro}"):
            with open(f"match/{koreanPro}/{jsonURL}") as json_file:
                json_data = json.load(json_file)

            participantId = findParticipantId(json_data, kPro)
            # print(participantId)
            #find participantId
            try:
                if json_data["queueId"] != 420:
                    raise IndexError
                time = json_data["gameId"]
                gameData = json_data["participants"][participantId]
                championName = data.getChampionName(gameData["championId"])
                spell1Id = data.getSpellName(gameData["spell1Id"])
                spell2Id = data.getSpellName(gameData["spell2Id"])

                # 7th item is ward or lens
                itemName = [data.getItemName(gameData["stats"][f"item{i}"]) for i in range(7)]
                runeName = [data.getRuneName(gameData["stats"][f"perk{i}"]) for i in range(6)]

                proCollection = pro[kPro]

                proCollection.insert_one({"_id": kPro})

                chamCollection = champion[championName]

                chamCollection.insert_one({"_id": championName}).inserted_id

            except IndexError:
                # json data get error 
                pass
            
            break
        break

if __name__ == "__main__":
    
    test()

# 모든데이터를 한글화하는데 성공했음 이제 어떻게할까?


# python3 matchInfByPro.py