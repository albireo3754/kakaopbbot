import pandas as pd
import os
import json
from pymongo import MongoClient
import pymongo
client = MongoClient()

pro = client["pro"]
champion = client["champion"]

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
    
            return pI["participantId"] 
class ProData:
    def __init__(self):
        self.prodata = pd.read_csv('nickplusID.csv',index_col= 0 ,header=0)
        self.koreanPros = self.prodata.loc[lambda df: df["country"] == "Korea" , ["name","team","nickname"]]
        
class DataDragon:
    def __init__(self):
        self.champion = self.getChampionData()
        self.spell = self.getSpellData()
        self.item = self.getItemData()
        self.rune = self.getRuneData()
        self.orrn = self.getOrrnData()
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

    def getOrrnData(self):
        with open("jsonCol/orrnItem.json") as json_file:
            json_data = json.load(json_file)
        return json_data
class GetData(DataDragon):
    
    #get key by int (3) return kname like "갈리오"
    def getChampionEName(self, key):
        return self.champion[str(key)]["ename"]

    def getChampionKName(self, key):
        return self.champion[str(key)]["kname"]

    def getSpellName(self, key):
        return self.spell[str(key)]["ename"]

    def getItemName(self, key):
        if key == 0:
            return None
        if key >= 7000:
            beforeOrrn = self.orrn[str(key)]["before"]
            return str(beforeOrrn)
        else:
            return str(key)

    def getRuneName(self, key):
        return self.rune[str(key)]["ename"]


def test():
    data = GetData()
    proData = ProData()
    for i in proData.koreanPros.index:
        proZip = proData.koreanPros.loc[i]
        #name = 시간빠르다앙,Kellin = nickname,Team =  Dynamics,
        name, team, nickname = proZip["name"], proZip["team"], proZip["nickname"]
        
        for jsonURL in os.listdir(f"match/{nickname}"):
            with open(f"match/{nickname}/{jsonURL}") as json_file:
                json_data = json.load(json_file)
            
            try:
                if json_data["queueId"] != 420:
                    continue
            except:
                continue

            participantId = findParticipantId(json_data, name)
            
            if participantId == None:
                continue
            
            # print(participantId)
            #find participantId
            try:
                time = json_data["gameCreation"]
                # print(participantId)
                gameData = json_data["participants"][participantId-1]
                # print(gameData)
                championEName = data.getChampionEName(gameData["championId"])
                championKName = data.getChampionKName(gameData["championId"])

                stats = gameData["stats"]
                spellName = [data.getSpellName(gameData[f"spell{i}Id"]) for i in range(1,3)]
                # 7th item is ward or lens
                itemName = [data.getItemName(gameData["stats"][f"item{i}"]) for i in range(7)]
                runeName = [data.getRuneName(gameData["stats"][f"perk{i}"]) for i in range(6)]
                statPerk = [str(gameData["stats"][f"statPerk{i}"]) for i in range(3)]

                (kill, deaths, assists) = (stats["kills"], stats["deaths"], stats["assists"])
                kda = f"{kill} / {deaths} / {assists}"

                proCollection = pro[nickname]
                proCollection.insert_one(
                {"_id": str(time), 
                "champion":{"en":championEName, "ko":championKName}, "statPerk": statPerk, 
                "proInf": {"name" : nickname, "team": team, "summonername": name},
                "spell":spellName, "itemName":itemName, "runeName":runeName, "kda": kda})

                chamCollection = champion[championKName]
                chamCollection.insert_one(
                {"_id": str(time), 
                "champion":{"en":championEName, "ko":championKName}, "statPerk": statPerk, 
                "proInf": {"name" : nickname, "team": team, "summonername": name},
                "spell":spellName, "itemName":itemName, "runeName":runeName, "kda": kda})
                
            except IndexError as e:
                print(f"error{nickname} and {e}")
                continue
                # json data get error 
            except pymongo.errors.DuplicateKeyError:
            # skip document because it already exists in new collection
                print(f"alread exist {nickname}")
                continue
            except Exception as e:
                print(e, jsonURL)

if __name__ == "__main__":
    
    test()

# 모든데이터를 한글화하는데 성공했음 이제 어떻게할까?


# python3 matchInfByPro.py