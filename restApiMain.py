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
    def makeOutput(self, outputs):
        return {"version": "2.0","template":{"outputs": outputs}}

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
        return {
            "title": f"{proInf['name']}({proInf['summonername']})",
            "description": f"{time} {kda}",
            "imageUrl": f"http://ddragon.leagueoflegends.com/cdn/10.25.1/img/item/.png",
            "altText" : f"{None}",
            "link": {
                "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
            }}
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
        if len(documents) == 0:
            return {"기록이없음을 알리는간단한 메시지~~ (나중에만들기)"}

        docs = [self.makeMatchListItem(document) for document in documents]
        output = self.makeListCard(f"{champName} 플레이 목록(최신순)", docs)
        

        return self.makeOutput(output)


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
        return self.makeOutput(output)

#이제 시간순서대로 나오게만하면되겟네
api.add_resource(Player, '/api/player/<pro_id>')
api.add_resource(Champion, '/api/champion/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
    