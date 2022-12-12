from start_game import Game, StartGame, PlayerStatistics


def register_user(email:str, name:str, surname:str) ->str:
    '''Register new user'''
    if check_if_user_exist(email=email, name=name, surname=surname) == False:
        new_user = StartGame(email=email, name=name, surname=surname)
        new_user.new_player()
        return "user been created"
    else:
        return "user already exist"


def check_if_user_exist(email:str, name:str, surname:str) -> bool:
    '''Check if user exist'''
    user = StartGame(email=email, name=name, surname=surname)
    return user.check_if_user_exist()


def get_user_current_game_status(game_id:str) -> list:
    '''return list of game data. When we open browser we will see game data'''
    status = Game(user_input="", game_id=game_id)
    return status.game_start_status()


def starting_game(name:str, surname:str, email:str) -> str:
    '''create new game in DB and return GAME_ID'''
    game = StartGame(name, surname, email)
    return game.new_game()


def hangman_game(user_input:str, game_id:str) -> list:
    '''return user input and game ID and it made changes to DB'''
    hangman = Game(user_input=user_input, game_id=game_id)
    hangman.update_db()
    return hangman.game_start_status() 


def get_statistic(email:str) -> list:
    '''return player statistic'''
    statistic = PlayerStatistics(email=email)
    return statistic.get_player_statistics()

