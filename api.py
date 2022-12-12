from flask import Flask , request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from control import*
from flask_cors import CORS
from flask import send_file
from typing import Union


app = Flask(__name__)
app = Flask("Hangman")
api = Api(app)
CORS(app) 

ERROR_MESSAGE = 'Request must be JSON'


class Test(Resource):
    def get(self):
        return "hello from Hangman server, you will die soon"


class Register(Resource):
    def post(self):
        if request.is_json:
            return register_user(name=request.json["name"], surname=request.json["surname"], email=request.json["email"])
        else:
            return ERROR_MESSAGE


class Login(Resource): 
    def post(self) -> Union[bool, tuple]:
        if request.is_json:
            return check_if_user_exist(name=request.json["name"], surname=request.json["surname"], email=request.json["email"])
        else:
            return ERROR_MESSAGE


class StartNewGame(Resource): 
    def post(self) -> bool:
        if request.is_json:
            return starting_game(name=request.json["name"], surname=request.json["surname"], email=request.json["email"])
        else:
            return ERROR_MESSAGE


class RegularGame(Resource):
    def post(self):
        if request.is_json:
            return hangman_game(user_input=request.json["user_input"], game_id=request.json["game_id"])
        else:
            return ERROR_MESSAGE


class GameStatus(Resource):
    def post(self):
        if request.is_json:
            status = get_user_current_game_status(game_id=request.json["game_id"])
            return [status[0], status[2], status[3], status[1], status[6]]
        else:
            return ERROR_MESSAGE


class Statistics(Resource):
    def post(self):
        if request.is_json:
            return get_statistic(email=request.json["email"])
        else:
            return ERROR_MESSAGE


api.add_resource(Test, '/test')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(StartNewGame, '/startnewgame')
api.add_resource(RegularGame, '/regulargame')
api.add_resource(GameStatus, '/gamestatus')
api.add_resource(Statistics, '/stats')


if __name__ == "__main__":
    app.run()