import sqlite3
import random
from sqlite3 import DatabaseError
from random_word import RandomWords
import logging


DATABASE_NAME = "testas"
ALPHABET_LETTERS = "abcdefghijklmnopqrstuvwxyz"
DB_NAME = "testas"
USERS_TABLE_NAME = "users"
GAMES_TABLE_NAME ="games"
DEFAULT_STATUS = "ongoing"
DEFAULT_SCORE = 10
DEFAULT_USER_GUESSES = 0


logging.basicConfig(filename="Hangman_game.log", encoding="UTF-8", level=logging.DEBUG)


class Game():
    def __init__(self, user_input, game_id) -> None:
        self.user_input = user_input
        self.conn = sqlite3.connect(DATABASE_NAME+".db")
        self.cursor = self.conn.cursor()
        with self.conn:
            self.cursor.execute(f"SELECT* From games WHERE id == '{game_id}'")
            fetch = self.cursor.fetchall()
        self.random_word = fetch[0][3]
        self.result = fetch[0][4]
        self.alphabet = fetch[0][5]
        self.guesed_letters = fetch[0][6]
        self.tries = fetch[0][7]
        self.upper_lower_letters = fetch[0][8]
        self.status = fetch[0][9]
        self.id = int(fetch[0][10])
        self.splitted_random_word = list(self.upper_lower_letters)
        self.loging()


    def modify_alphabet(self) -> str:
        return self.alphabet.replace(self.user_input, "")


    def lower_upper(self) -> str:
        for letter in range(len(self.splitted_random_word)):
            if self.splitted_random_word[letter] == self.user_input:
                self.splitted_random_word[letter] = self.user_input.upper()
        return "".join(self.splitted_random_word)


    def check_score(self) -> int:
        """It checks whether will user gets minus one point or not, if he made a right decision he will not get minus one point, 
        if he fail , he will get minus one"""
        user_score = -1
        for letter in self.random_word:
            if letter == self.user_input:
                user_score = 0
        return user_score


    def underscore_letters(self) -> str:
        """generates a string to display on web like ___a__a"""
        guesed_letter_list= []
        for letter in self.lower_upper():
            if letter.isupper() == True:
                guesed_letter_list.append(letter.lower())
            else:
                guesed_letter_list.append("_ ")
        guesed_letters = "".join(guesed_letter_list)
        return guesed_letters


    def check_status(self) -> str:
        guessed_letters = 0
        status = ""
        lower_upper = self.lower_upper()
        for x in lower_upper:
            if x.isupper() == True:
                guessed_letters += 1
        if len(lower_upper) <= guessed_letters and self.result > 0:
            status = "won"
        if (len(lower_upper) > guessed_letters and self.result > 0):
            status ="ongoing" 
        if (len(lower_upper) <= guessed_letters and self.result <= 1):
            status ="lost" 
        if (len(lower_upper) > guessed_letters and self.result <= 1):
            status ="lost" 
        return status


    def update_db(self) -> None:
        status = self.check_status()
        if status == "won" or status == "lost":
            alphabets = ""
        else:
            alphabets = self.modify_alphabet()
        with self.conn:
            self.cursor.execute(f"""UPDATE games SET 
            score = '{self.check_score() + self.result}', 
            available_alphabet_letters ='{alphabets}', 
            frontend_text ='{self.underscore_letters()}', 
            how_many_guesses_user_made ='{(self.tries) + 1 }',
            upper_lower_letters ='{self.lower_upper()}',
            status = '{status}'
            WHERE 
            id == '{self.id}'""")


    def game_start_status(self) -> list:
        game_data = []
        game_data.append(self.random_word)
        game_data.append(self.result)
        game_data.append(self.alphabet)
        game_data.append(self.guesed_letters)
        game_data.append(self.tries)
        game_data.append(self.upper_lower_letters)
        game_data.append(self.status)
        game_data.append(self.id)
        game_data.append(self.splitted_random_word)
        return game_data


    def loging(self) -> None:
        logging.info(f"""random world: {self.random_word},
        result: {self.check_score() + self.result} ,
        alphabet: {self.modify_alphabet()},
        tries: {self.tries + 1},
        u/lcases {self.lower_upper()},
        frontend text: {self.underscore_letters()},
        status {self.check_status()}""")



class StartGame():
    def __init__(self, name, surname, email) -> None:
        self.random_word = self.get_word()
        self.name = name
        self.surname = surname
        self.email = email
        self.conn = sqlite3.connect(DB_NAME+".db")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS '{USERS_TABLE_NAME}'(name text, surname text, email email)")
        except DatabaseError:
            print(f"Unable to create {USERS_TABLE_NAME} table! Database error.")
        except Exception as e:
            print(f"Unable to create table!. Error msg: {e}")

        try:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{GAMES_TABLE_NAME}'(
                name text,
                surname text,
                email email,
                random_word text,
                score integer,
                available_alphabet_letters text,
                frontend_text text,
                how_many_guesses_user_made integer,
                upper_lower_letters text,
                status text,
                id integer
                )""")
        except DatabaseError:
            print(f"Unable to create {GAMES_TABLE_NAME} table! Database error.")
        except Exception as e:
            print(f"Unable to create table!. Error msg: {e}")


    def id_generator(self) ->int:
        while True:
            random_id = random.randint(1111111, 9999999999)
            with self.conn:
                self.cursor.execute(f"SELECT id From {GAMES_TABLE_NAME} WHERE id =='{random_id}'")
                fetch = self.cursor.fetchall()
                if len(fetch) == 0:
                    break
        return random_id


    def get_word(self) -> str:
        random_word = RandomWords()
        return random_word.get_random_word()


    def get_underscores(self) -> str:
        return ("_ ") * (len(self.random_word))
  

    def check_if_user_exist(self) -> bool:
        user_exist = False
        with self.conn:
            self.cursor.execute(f"SELECT email From {USERS_TABLE_NAME} WHERE email =='{self.email}' and name =='{self.name}' and surname =='{self.surname}'")
            fetch = self.cursor.fetchall()
            if len(fetch) > 0 and (''.join(fetch[0])) == self.email:
                user_exist = True
        return user_exist


    def new_player(self) -> None:
        """Creates a new player in DB"""
        if self.check_if_user_exist() == False:
            with self.conn:
                self.cursor.execute(f"""INSERT INTO {USERS_TABLE_NAME} VALUES (
                '{self.name}',
                '{self.surname}',
                '{self.email}'
                )""")


    def new_game(self) -> int:
        """Creates a new game in DB"""
        game_id = self.id_generator()
        with self.conn:
            self.cursor.execute(f"""INSERT INTO {GAMES_TABLE_NAME} 
            VALUES ('{self.name}',
            '{self.surname}',
            '{self.email}',
            '{self.random_word}',
            '{DEFAULT_SCORE}',
            '{ALPHABET_LETTERS}' ,
            '{self.get_underscores()}',
            '{DEFAULT_USER_GUESSES}',
            '{self.random_word}',
            '{DEFAULT_STATUS}',
            '{game_id}'
            )""")
        return game_id


class PlayerStatistics():
    def __init__(self, email) -> None:
        self.conn = sqlite3.connect(DATABASE_NAME+".db")
        self.cursor = self.conn.cursor()
        self.email = email

    def get_player_statistics(self) -> list:
        with self.conn:
            self.cursor.execute(f"SELECT count(status) From {GAMES_TABLE_NAME} WHERE email == '{self.email}' and status=='won'")
            player_won = self.cursor.fetchall()[0][0]
        with self.conn:
            self.cursor.execute(f"SELECT count(status) From {GAMES_TABLE_NAME} WHERE email == '{self.email}' and status=='lost'")
            player_lost = self.cursor.fetchall()[0][0]
        with self.conn:
            self.cursor.execute(f"SELECT count(status) From {GAMES_TABLE_NAME} WHERE email == '{self.email}' and status=='ongoing'")
            player_not_finished = self.cursor.fetchall()[0][0]
        return [player_won, player_lost, player_not_finished]





if __name__=="__main__":
    # zz = game(user_input="s", game_id=4422979748)
    # aa = zz.update_db()
    # ss = zz.loging()
    # lol = start_game("aallh", "surname", "email@lt.lt")
    # answ = lol.new_game()
    stat = PlayerStatistics(email="pa@lt.lt")