from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from pymongo import MongoClient 
import json
app = Flask(__name__)
api = Api(app)


# parser = reqparse.RequestParser()
# parser.add_argument('action', action='append')
class Data:
    CLIENT = MongoClient("mongodb://localhost:27017/")
    PLAYER = CLIENT["pro"]
    CHAMPION = CLIENT["champion"]

    def findOne(self, name):
        return self.CHAMPION[name].find_one()



class Player(Resource):

    def post(self, pro_id):
        return TODOS[todo_id]

    #kakaoAPI에서는 사용하지않음
    # def get(self, todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     return TODOS[todo_id]
    
    # def delete(self, todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     del TODOS[todo_id]
    #     return '', 204
    
    # def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201
todos = {}

def makeoutput(item):
    return {
            "title": item,
            "description": item,
            "imageUrl": f"http://ddragon.leagueoflegends.com/cdn/10.25.1/img/item/{item}.png",
            "link": {
                "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
            }
            }
def output(items):
    
    return {
            "version": "2.0",
            "template":{
                "outputs": [{
                    "listCard": {
                        "header": {"title": "아이템"},
                        "items": [makeoutput(item) for item in items]
                        }}]}
            }

class Champion(Resource):
    
    def post(self):
        data = Data()
        # args = parser.parse_args()
        jsonData = request.get_json()
        print(jsonData)
        action = jsonData['action']
        param = action['params']
        champName = param['champion']
        print(champName)
        rune = data.findOne(champName)["itemName"]
        print(rune)
        return output(rune)
        # return {"version": "2.0",
        #         "template": {
        #         "outputs": [
        #         {
        #             "simpleText": 
        #             {
        #                 "text": f"{champName} 아이템은 {rune} 입니다."
        #             }
        #         }
        #         ]}}


        # args = parser.parse_args()
        # todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        # todo_id = f'todo{todo_id}'
        # TODOS[todo_id] = {'task': args['task']}
        # return TODOS[todo_id], 201

api.add_resource(Player, '/api/player/<pro_id>')
api.add_resource(Champion, '/api/champion/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
    