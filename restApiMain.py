from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from pymongo import MongoClient 
import json
from datetime import datetime
app = Flask(__name__)
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
        if context is None:
            return {"version": "2.0","template":{"outputs": outputs}}
        return {"version": "2.0","template":{"outputs": outputs}, "context":{"values": contexts}}
    def makeQuickReply(self, replies):
        return {"version": "2.0","template":{"quickReplies": replies}}

    #headerTitle is string, items is list of item
    def makeListCard(self, headerTitle, items, buttons=None):
        return [{"listCard":
                    {"header": {"title": headerTitle},
                    "items": items,
                    "buttons": buttons}}]

    def makeListItem(self, item):
        return {
            "title": f"{item}",
            "description": f"{item}",
            "imageUrl": f"http://ddragon.leagueoflegends.com/cdn/10.25.1/img/item/{item}.png",
            "altText" : f"{item}",
            "link": {
                "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
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
        print(description)
        return {
            "title": title,
            "description": description,
            "thumbnail":{
                "imageUrl": thumbnail
            },
            "buttons":buttons
        }
    
    def makeIntroCard(self, doc, buttons, cardFunc):
        time = datetime.fromtimestamp(int(doc['_id'])//1000).strftime('%m-%d/%H:%M')
        kda = doc["kda"]
        proInf = doc['proInf']
        Domination = doc['runeDetail'][0]['color']
        Electrocute = doc['runeName'][0]

        title = f"{proInf['name']}({proInf['summonername']})"
        description = f"Kda:{kda} Time: {time}"
        thumbnail = f"http://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/{Domination}/{Electrocute}/{Electrocute}.png"
            
        return cardFunc(title,description,thumbnail,buttons)
    def makeButton(self, label, action, messageText):
        return {
            "label": label,
            "action": action,
            "messageText": messageText
        }

    def makeButtons(self):
        runeButton = self.makeButton(label="룬 보러가기",action="message",messageText="룬이요")
        itemButton = self.makeButton(label="최종아이템 보러가기",action="message",messageText="아이템이요")
        skillButton = self.makeButton(label="스킬트리 보러가기",action="message",messageText="스킬트리요")
        return [runeButton,itemButton,skillButton]
    def makeThmbnail(self, imageUrl):
        return {
            "imageUrl": imageUrl
        }
    
    def makeSimpleText(self, text):
        return {
            "simpleText": {"text": text}
        }

class Player(Resource):
    def __init__(self):
        pass

class Champion(Resource, Bot):
    
    def post(self):
        data = Data()
        # args = parser.parse_args()
        jsonData = request.get_json()
        # print(jsonData)
        action = jsonData['action']
        param = action['params']
        champName = param['champion']
        # print(champName)
        documents = data.findList(champName)
        print(3)
        if len(documents) == 0:
            print(4)
            output = self.makeSimpleText("그런건 아무도 안해요 ㅠㅠ")
            return self.makeSkillResponse(output)
        
        buttons = self.makeButtons()

        basicCards = [self.makeIntroCard(doc, buttons, self.makeBasicCard) for doc in documents]

        output = self.makeCarousel(basicCards)
        print(output)
        return self.makeSkillResponse(output)



class Champion_v2(Resource, Bot):
    
    
    def post(self):
        data = Data()
        # args = parser.parse_args()
        jsonData = request.get_json()

        # print(jsonData)
        action = jsonData['action']
        param = action['params']
        champName = param['champion']
        # print(champName)

        documents = data.findList(champName)
        if len(documents) == 0:
            return {"기록이없음을 알리는간단한 메시지~~ (나중에만들기)"}

        docs = [self.makeMatchListItem(document) for document in documents]

        output = self.makeListCard(f"{champName} 플레이 목록(최신순)", docs)
        
        return self.makeSkillResponse(output)


class Champion_v1(Resource, Bot):
    
    
    def post(self):
        data = Data()
        # args = parser.parse_args()
        jsonData = request.get_json()
        # print(jsonData)
        action = jsonData['action']
        param = action['params']
        champName = param['champion']
        # print(champName)

        try:
            runes = data.findOne(champName)["itemName"]
        except:
            print(data.findOne(champName))
            return {}

        items = [self.makeListItem(rune) for rune in runes]
        output = self.makeListCard("itemlist", items)
        
        print(items)
        return self.makeSkillResponse(output)


#이제 시간순서대로 나오게만하면되겟네
api.add_resource(Player, '/api/player/<pro_id>')
api.add_resource(Champion, '/api/champion/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
    