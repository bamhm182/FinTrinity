from re import sub, findall
from json import dumps


class Game:
    def __init__(self):
        self.id = ""
        self.title = ""
        self.path = ""
        self.image = ""

    def set_id(self, game_id):
        self.id = game_id

    def set_path(self, path):
        self.path = f"{path}/{self.id}"
        self.image = f"{self.path}/sce_sys/icon0.png"
        self.set_title()

    def set_title(self):
        try:
            with open(f'{self.path}/sce_sys/param.sfo') as fp:
                clean = sub(".u[0-9a-f]{4}", "", dumps(fp.read()))
                self.title = findall("([A-Za-z -]{5,})", clean)[-1]
        except FileNotFoundError or UnicodeDecodeError:
            self.title = "Unknown"
