from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from pymongo import MongoClient 
import json
from datetime import datetime
from flask_cors import CORS
from base import BASE_DIR
app = Flask(__name__)
CORS(app)
api = Api(app)

import pymongo

# parser = reqparse.RequestParser()
# parser.add_argument('action', action='append')

class Data:
    CLIENT = MongoClient("mongodb://localhost:27017/")
    PLAYER = CLIENT["pro"]
    CHAMPION = CLIENT["champion"]
    
    def findList(self, name):
        lists = []
        for i in self.CHAMPION[name].find().sort("_id", pymongo.DESCENDING).limit(5):
            lists.append(i)

        return lists

    def findOne(self, name):
        return self.CHAMPION[name].find_one()


class Bot:
    #output will be [{"listcard": ~~}]
    def makeSkillResponse(self, outputs, contexts = None):
        if type(outputs) is not list:
            outputs = [outputs]
        if contexts is None:
            return {"version": "2.0","template":{"outputs": outputs}}
        
        if type(contexts) is not list:
            contexts = [contexts]
        return {"version": "2.0","template":{"outputs": outputs}, "context":{"values": contexts}}
    
    def makeQuickReply(self, replies):
        return {"version": "2.0","template":{"quickReplies": replies}}

    #headerTitle is string, items is list of item
    def makeListCard(self, headerTitle, items, buttons=None):
        return [{"listCard":
                    {"header": {"title": headerTitle},
                    "items": items,
                    "buttons": buttons}}]

    def makeListItem(self, title, description, imageUrl):
        return {
            "title": f"{title}",
            "description": f"{description}",
            "imageUrl": f"{imageUrl}",
            "altText" : f"{title}",
            "link": {
                "web": f"https://namu.wiki/w/{title}"
            }}
    
    def makeMatchListItem(self, doc):
        time = datetime.fromtimestamp(int(doc['_id'])//1000).strftime('%m-%d/%H:%M')
        kda = doc["kda"]
        proInf = doc['proInf']
        Domination = doc['runeDetail'][0]['color']
        Electrocute = doc['runeName'][0]

        return {
            "title": f"{proInf['name']}({proInf['summonername']})",
            "description": f"Kda:{kda} , Time: {time}",
            "imageUrl": f"http://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/{Domination}/{Electrocute}/{Electrocute}.png",
            "altText" : f"{None}",
            "link": {
                "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
            }}

    def makeCarousel(self, items, _type = "basicCard"):
        """[summary]

        Arguments:
            items {[list]} -- [max 10, basicCard list]

        Keyword Arguments:
            _type {str} -- [description] (default: {"basicCard"})

        Returns:
            [type] -- [description]
        """
        return {"carousel":{"type": _type, "items": items}}
    
    def makeBasicCard(self, title, description, thumbnail, buttons):
        return {
            "title": title,
            "description": description,
            "thumbnail":{
                "imageUrl": thumbnail
            },
            "buttons":buttons
        }
    
    def makeIntroCard(self, doc, buttons, cardFunc):
        kda = doc["kda"]
        proInf = doc['proInf']
        Domination = doc['runeDetail'][0]['color']
        Electrocute = doc['runeName'][0]
        version = doc['version']

        title = f"{proInf['name']}({proInf['summonername']})"
        description = f"Kda:{kda} version: {version}"
        thumbnail = f"http://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/{Domination}/{Electrocute}/{Electrocute}.png"
            
        return cardFunc(title,description,thumbnail,buttons)
    def makeButton(self, label, action, messageText):
        return {
            "label": label,
            "action": action,
            "messageText": messageText
        }

    
    def makeThmbnail(self, imageUrl):
        return {
            "imageUrl": imageUrl
        }
    
    def makeSimpleText(self, text):
        return {
            "simpleText": {"text": text}
        }

    def makeContext(self, name, params, lifeSpan = 5, ttl = 60):
        """[summary]

        Arguments:
            name {string} -- [description]
            lifeSpan {int} -- [description]
            params {dict} -- [description]

        Returns:
            context
        """
        return {
            "name": name,
            "lifeSpan": lifeSpan,
            "ttl": ttl,
            "params": params
        }
    def makeRISButtons(self, idx):
        runeButton = self.makeButton(label="룬 보러가기",action="message",messageText=f"{idx}번 선수의 룬")
        itemButton = self.makeButton(label="최종아이템 보러가기",action="message",messageText=f"{idx}번 선수의 아이템")
        skillButton = self.makeButton(label="스킬트리 보러가기",action="message",messageText=f"{idx}번 선수의 스킬트리")
        return [runeButton,itemButton,skillButton]
    def makeSkillText(self, keys):
        timeLineText = ''
        
        for idx, val in enumerate(keys):
            skill = ''
            if val == 1:
                skill = 'Q'
            elif val == 2:
                skill = 'W'
            elif val == 3:
                skill = 'E'
            elif val == 4:
                skill = 'R'
            
            timeLineText += f'{idx+1}레벨{skill} -> '
        return timeLineText
    def makeStatText(self, keys):
        statText = ''

        for key in keys:
            if key == "5001":
                stat = '체력'
            elif key == "5002":
                stat = '물방'
            elif key == "5003":
                stat = '마저'
            elif key == "5005":
                stat = '공속'
            elif key == "5007":
                stat = '주문가속'
            elif key == "5008":
                stat = '적응형'
            statText += f'{stat} / ' 

        return statText
class Player(Resource):
    def __init__(self):
        pass

class Champion(Resource, Bot):
    
    def post(self):
        data = Data()
        # args = parser.parse_args()
        jsonData = request.get_json()
        print(request.content_type)
        print(jsonData)
        file_path = f"{BASE_DIR}/sample.json"

        with open(file_path, 'w') as outfile:
            json.dump(jsonData, outfile, indent=2)
        # print(jsonData)
        action = jsonData['action']
        params = action['params']
        champName = params['champion']
        # print(champName)
        documents = data.findList(champName)
        if len(documents) == 0:
            output = self.makeSimpleText("그런건 아무도 안해요 ㅠㅠ")
            return self.makeSkillResponse(output)
        
        
        basicCards = []
        contexts = []
        for idx,doc in enumerate(documents):
            basicCards.append(self.makeIntroCard(doc, self.makeRISButtons(idx+1), self.makeBasicCard))
            contexts.append(self.makeContext(f"select_champion_{idx+1}", 
            {"runeName": doc['runeName'], 
            "runeDetail": doc['runeDetail'],
            "itemKey": doc['itemName'],
            "skill": doc['skill'],
            "statPerk": doc['statPerk']}))
        
        output = self.makeCarousel(basicCards)

        a = self.makeSkillResponse(output, contexts)
        file_path = f"{BASE_DIR}/sample.json"

        with open(file_path, 'w') as outfile:
            json.dump(a, outfile, indent=2)
        return self.makeSkillResponse(output, contexts)

class Rune(Resource, Bot):
    def post(self):
        jsonData = request.get_json()
        file_path = f"{BASE_DIR}/Rune.json"
        with open(file_path, 'w') as outfile:
            json.dump(jsonData, outfile, indent=2)

        order = jsonData['action']['params']['sys_number_ordinal']
        idx = json.loads(order)["amount"] - 1

        params = jsonData['contexts'][idx]['params']
        
        runeName = json.loads(params['runeName']['value'])
        runeDetail = json.loads(params['runeDetail']['value'])
        statPerk = json.loads(params['statPerk']['value'])
        itemsMain = []
        for eName, detail in zip(runeName[:4],runeDetail[:4]):
            title = detail['kname']
            description = eName
            iconUrl = detail['iconUrl']

            imageUrl = f"http://ddragon.leagueoflegends.com/cdn/img/{iconUrl}"
            itemsMain.append(self.makeListItem(title, description, imageUrl))
        itemsSub = []
        for eName, detail in zip(runeName[4:],runeDetail[4:]):
            title = detail['kname']
            description = eName
            iconUrl = detail['iconUrl']

            imageUrl = f"http://ddragon.leagueoflegends.com/cdn/img/{iconUrl}"
            itemsSub.append(self.makeListItem(title, description, imageUrl))
        
        # documents is from context
        
        outputMain = self.makeListCard(headerTitle = "메인룬 목록입니다.", items= itemsMain)
        outputSub = self.makeListCard(headerTitle = "서브룬입니다.", items= itemsSub)
        statText = self.makeStatText(statPerk)
        outputStat = self.makeSimpleText(statText)
        output = outputMain + outputSub + [outputStat]
        return self.makeSkillResponse(output)

class Item(Resource, Bot):
    def post(self):
        jsonData = request.get_json()
        file_path = f"{BASE_DIR}/Item.json"
        with open(file_path, 'w') as outfile:
            json.dump(jsonData, outfile, indent=2)
        order = jsonData['action']['params']['sys_number_ordinal']
    
        idx = json.loads(order)["amount"] - 1

        params = jsonData['contexts'][idx]['params']
        itemKey = json.loads(params['itemKey']['value'])

        with open("jsonCol/item.json") as json_file:
            json_item = json.load(json_file)
        
        items1 =[]
        items2 =[]
        
        cnt = 0
        for key in itemKey :
            if key == None:
                break
            url = f"http://ddragon.leagueoflegends.com/cdn/10.25.1/img/item/{key}.png"
            if cnt<3:
                items1.append(self.makeListItem(json_item[key]["kname"],json_item[key]["kname"],url))
            else:
                items2.append(self.makeListItem(json_item[key]["kname"],json_item[key]["kname"],url))
            cnt+=1    

        
        output1 = self.makeListCard(headerTitle="윗줄", items = items1)
        output2 = self.makeListCard(headerTitle="아랫줄", items = items2)
    
        output = output1 + output2
        return self.makeSkillResponse(output)

class Skill(Resource, Bot):
    def post(self):
        jsonData = request.get_json()
        file_path = f"{BASE_DIR}/Skill.json"
        with open(file_path, 'w') as outfile:
            json.dump(jsonData, outfile, indent=2)
        order = jsonData['action']['params']['sys_number_ordinal']
    
        idx = json.loads(order)["amount"] - 1

        params = jsonData['contexts'][idx]['params']
        skillKey = json.loads(params['skill']['value'])

        skillText = self.makeSkillText(skillKey)
        
        output = self.makeSimpleText(skillText)
        return self.makeSkillResponse(output)
#1. 룬페이지 작성법을 연구하자
#2. 룬 목록을 현재로 ["commet"] 으로 받는데 이걸로 받으면 비효율적이지않나? - 일단 청사진을 그려보는게 좋겟네.

api.add_resource(Player, '/api/player/<pro_id>')
api.add_resource(Champion, '/api/champion/')
api.add_resource(Rune, '/api/rune/')
api.add_resource(Item, '/api/item/')
api.add_resource(Skill, '/api/skill/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
    