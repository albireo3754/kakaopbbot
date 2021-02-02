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
            
            return pI.get("participantId")
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

    def getMatchJson(self,url):
        with open(url) as json_file:
            time_data = json.load(json_file)
        return time_data
    def getTimelineJson(self,url):
        with open(url) as json_file:
            json_data = json.load(json_file)
        return json_data

class GetData(DataDragon):
    
    #get key by int (3) return kname like "갈리오"
    def makeChampionEName(self, key):
        return self.champion[str(key)]["ename"]

    def makeChampionKName(self, key):
        return self.champion[str(key)]["kname"]

    def makeSpellName(self, key):
        return self.spell[str(key)]["ename"]

    def makeItemName(self, key):
        if key == 0:
            return None
        if key >= 7000:
            beforeOrrn = self.orrn[str(key)]["before"]
            return str(beforeOrrn)
        else:
            return str(key)

    def makeRuneName(self, key):
        return self.rune[str(key)]["ename"]

    def makeRuneName_v2(self, key):
        return {
            "kname" : self.rune[str(key)]["kname"], 
            "color": self.rune[str(key)]["color"],
            "iconUrl": self.rune[str(key)]["iconUrl"]}

    def makeKda(self, stats):
        (kill, deaths, assists) = (stats["kills"], stats["deaths"], stats["assists"])
        kda = f"{kill} / {deaths} / {assists}"
        return kda
    
    def makeVersion(self, json_data):
        versions = json_data['gameVersion'].split('.')
        version= versions[0]+'.'+versions[1]
        return version
    
    def makeSkillTimeline(self, json_data, Id):
        eventsList = json_data['frames'][1:]
        skillslot = []
        for events in eventsList:
            for event in events['events']:
                # type : ITEM_PURCHASED, ITEM_SOLD, ITEM_UNDO, SKILL_LEVEL_UP
                if event.get('participantId') != Id:
                    continue
                if event.get('type') == 'SKILL_LEVEL_UP':
                    skillslot.append(event.get('skillSlot'))

        return skillslot
class Query(GetData):
    def __init__(self):
        super().__init__()  
        self.proData = ProData()
    def make(self):
        
        for i in self.proData.koreanPros.index:
            proZip = self.proData.koreanPros.loc[i]
            #name = 시간빠르다앙,Kellin = nickname,Team =  Dynamics,
            name, team, nickname = proZip["name"], proZip["team"], proZip["nickname"]
            
            for jsonURL in os.listdir(f"match/{nickname}"):
                print(jsonURL,"is")
                try:
                    json_data = self.getMatchJson(f"match/{nickname}/{jsonURL}")
                    time_data = self.getTimelineJson(f"timeline/{nickname}/{jsonURL}")
                except:
                    print(f"match/{nickname}/{jsonURL}")
                    print(f"timeline/{nickname}/{jsonURL}")
                    continue
                
                
                if json_data.get("queueId") != 420:
                    continue
            
                participantId = findParticipantId(json_data, name)
                
                if participantId == None:
                    continue
                
                # print(participantId)
                #find participantId
                try:
                    time = json_data["gameCreation"]
                    # print(participantId)
                    gameData = json_data["participants"][participantId]
                    # print(gameData)
                    championEName = self.makeChampionEName(gameData["championId"])
                    championKName = self.makeChampionKName(gameData["championId"])

                    
                    spellName = [self.makeSpellName(gameData[f"spell{i}Id"]) for i in range(1,3)]
                    # 7th item is ward or lens

                    itemName = [self.makeItemName(gameData["stats"][f"item{i}"]) for i in range(7)]
                    runeName = [self.makeRuneName(gameData["stats"][f"perk{i}"]) for i in range(6)]
                    statPerk = [str(gameData["stats"][f"statPerk{i}"]) for i in range(3)]
                    runeDetail = [self.makeRuneName_v2(gameData["stats"][f"perk{i}"]) for i in range(6)]
                    kda = self.makeKda(gameData["stats"])
                    version = self.makeVersion(json_data)
                    
                    skill = self.makeSkillTimeline(time_data,participantId)
                    # proCollection = pro[nickname]
                    # proCollection.insert_one(
                    # {"_id": str(time), 
                    # "champion":{"en":championEName, "ko":championKName}, "statPerk": statPerk, 
                    # "proInf": {"name" : nickname, "team": team, "summonername": name},
                    # "spell":spellName, "itemName":itemName, "runeName":runeName, "kda": kda,
                    # "runeDetail": runeDetail, "version": version})
                    print(skill)
                    chamCollection = champion[championKName]
                    chamCollection.insert_one(
                    {"_id": str(time), 
                    "champion":{"en":championEName, "ko":championKName}, "statPerk": statPerk, 
                    "proInf": {"name" : nickname, "team": team, "summonername": name},
                    "spell":spellName, "itemName":itemName, "runeName":runeName, "kda": kda,
                    "runeDetail": runeDetail, "version": version, "skill": skill})
                    print(jsonURL)
                except IndexError as e:
                    print(f"error{nickname} and {e}")
                    continue
                    # json self get error 
                except pymongo.errors.DuplicateKeyError:
                # skip document because it already exists in new collection
                    print(f"alread exist {nickname}")
                    continue
                except Exception as e:
                    print(e, jsonURL)

    def update(self):

        self = GetData()
        self.proData = ProData()
        for i in self.proData.koreanPros.index:
            proZip = self.proData.koreanPros.loc[i]
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
                    # print(participantId)
                    gameData = json_data["participants"][participantId-1]
                    # print(gameData)
                    championKName = self.makeChampionKName(gameData["championId"])
                    
                    kda = self.makeKda(gameData["stats"])
                    version = self.makeVersion(json_data)
                    proCollection = pro[nickname]
                    proCollection.update_one({},{'$set' : {"kda":kda}},upsert=False)

                    chamCollection = champion[championKName]
                    chamCollection.update_one({},{'$set' : {"kda":kda}},upsert=False)
                    
                    print(jsonURL)
                except IndexError as e:
                    print(f"error{nickname} and {e}")
                    continue
                    # json self get error 
                except pymongo.errors.DuplicateKeyError:
                # skip document because it already exists in new collection
                    print(f"alread exist {nickname}")
                    continue
                except Exception as e:
                    print(e, jsonURL)

if __name__ == "__main__":
    query = Query()
    query.make()
    # make()
# 모든데이터를 한글화하는데 성공했음 이제 어떻게할까?


# python3 matchInfByPro.py