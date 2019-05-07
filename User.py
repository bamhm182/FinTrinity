from urllib import request
from re import findall
import os
from Game import Game


class User:
    def __init__(self):
        self.id = ""
        self.decrypt_key = ""
        self.name = ""
        self.path = ""
        self.games = []

    def set_id(self, account_id):
        self.id = account_id
        with request.urlopen(f'http://cma.henkaku.xyz/?aid={account_id}') as response:
            self.decrypt_key = findall(f"{account_id}</b>: ([A-Za-z0-9]*)", str(response.read()))[0]

    def set_name(self, name):
        self.name = name

    def set_path(self, path):
        self.path = f"{path}/{self.id}"
        self.get_games()

    def get_games(self):
        a = [s for s in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, s))]
        a.sort(reverse=True, key=lambda s: os.path.getmtime(os.path.join(self.path, s)))
        for folder in a:
            game_id = findall(r"([A-Z]{4}[0-9]{5})$", folder)[0]
            if game_id:
                game = Game()
                game.set_id(game_id)
                game.set_path(self.path)
                self.games.append(game)
