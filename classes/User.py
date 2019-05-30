from urllib import request
from re import findall
import os
from classes.Game import Game
import sys


class User:
    def __init__(self):
        self.id = ""
        self.decrypt_key = ""
        self.name = ""
        self.path = ""
        self.games = []

    def set_id(self, account_id):
        try:
            self.id = account_id
            with request.urlopen(f'http://cma.henkaku.xyz/?aid={account_id}') as response:
                self.decrypt_key = findall(f"{account_id}</b>: ([A-Za-z0-9]*)", str(response.read()))[0]
        except IndexError:
            print("Invalid Account ID or cma.henkaku.xyz malfunctioning.")
            sys.exit("Invalid Account ID")

    def set_name(self, name):
        self.name = name

    def set_path(self, path):
        self.path = path / self.id

        if not os.path.exists(self.path):
            print(f"{self.path} does not exist. Please ensure you have run QCMA and backed up your game.")
            sys.exit("User Path Does Not Exist")

        self.get_games()

    def get_games(self):
        a = [s for s in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, s))]

        if len(a) == 0:
            print(f"{self.path} contains no games. Please ensure you have run QCMA and backed up your game.")
            sys.exit("No Game In User Path")

        a.sort(reverse=True, key=lambda s: os.path.getmtime(os.path.join(self.path, s)))
        for folder in a:
            game_id = findall(r"([A-Z]{4}[0-9]{5})$", folder)
            if game_id:
                game = Game()
                game.set_id(game_id[0])
                game.set_path(self.path)
                self.games.append(game)
