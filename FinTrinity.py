from pathlib import Path
import os
import shutil
from urllib import request
from zipfile import ZipFile
import re
import games
from utils import make_copy, make_dir, read_hkcu
import datetime


class FinTrinity:
    def __init__(self):
        # Read from Registry
        account = read_hkcu(r"Software\codestation\qcma", 'lastAccountId')
        username = read_hkcu(r"Software\codestation\qcma", 'lastOnlineId')
        apps_path = read_hkcu(r"Software\codestation\qcma", 'appsPath') + '/PGAME'
        game_id = self.get_game_id(f"{apps_path}/{account}")

        if game_id:
            question = f"Found {games.lst[game_id]} ({game_id}) for user {username} ({account}). Continue? (yes/no): "
            if not input(question)[0] == "y":
                exit()
        else:
            print(f"No compatible games found for {username} ({account})")
            exit()

        # Setup Folders
        now = datetime.datetime.now()
        timestamp=f"{now.year}{now.month}{now.day}-{now.hour}{now.minute}{now.second}"
        working_dir = f"{Path.home()}/Desktop/FinTrinity{timestamp}"
        decrypt_dir = f"{working_dir}/NPUG80318.decrypted"
        hack_dir = f"{working_dir}/NPUG80318.hacked"
        backup_dir = f"{working_dir}/NPUG80318.backup"
        original_dir = f"{apps_path}/{account}/{game_id}"

        # Setup User Information
        decrypt_key = self.get_decrypt_key(account)

        if decrypt_key:
            print(f"Got Decryption Key for {username} ({account}): {decrypt_key}")
        else:
            print(f"Unable to get Decryption Key for {username} ({account})")
            exit()

        # Backup Game
        print(f"Creating Working Directory in: {working_dir}")
        make_dir(working_dir)
        make_copy(original_dir, backup_dir)
        make_copy(original_dir, decrypt_dir)

        # Download Dependencies
        print(f"Downloading and Extracting Dependencies")
        self.download(working_dir)
        self.extract_psvimgtools(working_dir, decrypt_dir)

        # Hack
        print(f"Applying Trinity Hack:\n\n\n")
        self.decrypt_game(decrypt_key, decrypt_dir)
        self.encrypt_game(decrypt_key, decrypt_dir, hack_dir)
        self.replace_folder(hack_dir, original_dir)

        print(f"\n\n\nTrinity Applied. Please refresh your QCMA database and transfer your game back to your Vita")
        input("[PRESS ENTER TO CLOSE]")

    @staticmethod
    def get_game_id(root):
        for f in os.listdir(root):
            if f in games.lst:
                return f

    @staticmethod
    def get_decrypt_key(aid):
        with request.urlopen(f'http://cma.henkaku.xyz/?aid={aid}') as response:
            return re.findall(f"{aid}</b>: ([A-Za-z0-9]*)", str(response.read()))[0]

    @staticmethod
    def download(dst):
        request.urlretrieve('https://github.com/TheOfficialFloW/Trinity/releases/download/v1.0/PBOOT.PBP',
                            f'{dst}/PBOOT.PBP')

        request.urlretrieve('https://github.com/yifanlu/psvimgtools/releases/download/v0.1/psvimgtools-0.1-win64.zip',
                            f'{dst}/psvimgtools-0.1-win64.zip')

    @staticmethod
    def extract_psvimgtools(src, dst):
        with ZipFile(f'{src}/psvimgtools-0.1-win64.zip', 'r') as z:
            z.extractall(dst)

    @staticmethod
    def decrypt_game(key, src):
        os.chdir(src)
        os.system(f'psvimg-extract -K {key} game/game.psvimg game_dec')
        make_copy(f'{src}/../PBOOT.PBP',
                  f'{src}/game_dec/ux0_pspemu_temp_game_PSP_GAME_NPUG80318/PBOOT.PBP')

    @staticmethod
    def encrypt_game(key, src, dst):
        make_dir(f'{dst}/game')
        os.chdir(src)
        os.system(f'psvimg-create -n game -K {key} game_dec {dst}/game')

        make_copy(f'{src}/license', f'{dst}/license')
        make_copy(f'{src}/sce_sys', f'{dst}/sce_sys')

    @staticmethod
    def replace_folder(src, dst):
        shutil.rmtree(dst)
        make_copy(src, dst)


it = FinTrinity()
