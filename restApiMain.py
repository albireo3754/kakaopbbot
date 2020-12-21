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
        return {"version": "2.0",
                "template": {
                "outputs": [
                {
                    "simpleText": 
                    {
                        "text": f"아칼리 룬은 {data.findOne(champName)["runeName"]}"
                    }
                }
                ]}}


        # args = parser.parse_args()
        # todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        # todo_id = f'todo{todo_id}'
        # TODOS[todo_id] = {'task': args['task']}
        # return TODOS[todo_id], 201

api.add_resource(Player, '/api/player/<pro_id>')
api.add_resource(Champion, '/api/champion/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
    