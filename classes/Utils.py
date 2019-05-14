import os
import shutil
import winreg
from urllib import request
from zipfile import ZipFile
import datetime
from pathlib import Path
import sys


def decrypt_game(key, src, pboot, game_id):
    print("Decrypting:\n")
    os.chdir(src)
    command = f'psvimg-extract -K {key} game/game.psvimg game_dec'
    print(command)
    if os.system(command) != 0:
        print("Decryption failed with the above information.")
        sys.exit("Decryption Failed")
    shutil.copyfile(pboot, src / 'game_dec' / f'ux0_pspemu_temp_game_PSP_GAME_{game_id}' / 'PBOOT.PBP')


def encrypt_game(key, src, dst):
    print("\nEncrypting:\n")
    os.chdir(src)
    command = f'psvimg-create -n game -K {key} game_dec "{dst}/game"'
    print(command)
    if os.system(command) != 0:
        print("Game Creation failed with the above information.")
        sys.exit("Game Creation Failed")

    shutil.copytree(src / 'license', dst / 'license')
    shutil.copytree(src / 'sce_sys', dst / 'sce_sys')


def make_dir(d):
    d = Path(d)
    if not os.path.exists(d):
        os.makedirs(d)
    return d


def read_hkcu(key: str, val: str):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_READ) as key:
        return winreg.QueryValueEx(key, val)[0]


def download(url, dst):
    request.urlretrieve(url, f'{dst}/{url.split("/")[-1]}')


def get_timestamp():
    now = datetime.datetime.now()
    return f"{now.year}{now.month}{now.day}-{now.hour}{now.minute}{now.second}"


def replace_folder(src, dst):
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except PermissionError or OSError:
        input(f"\nIt appears you have the following folder open:\n{dst}\n\nPlease close it and press Enter...")
        replace_folder(src, dst)


def extract(src, dst):
    with ZipFile(src, 'r') as z:
        z.extractall(dst)


def get_home():
    return Path.home()
