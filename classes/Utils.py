import os
import shutil
from urllib import request
from zipfile import ZipFile
import datetime
from pathlib import Path
import sys
import platform
import stat
from subprocess import call


def decrypt_game(key, src, pboot, game_id):
    print("Decrypting:\n")
    os.chdir(src)
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.chmod("./psvimg-extract", stat.S_IRWXU)
    command = [str(Path("psvimg-extract").absolute()), "-K", key, "game/game.psvimg", "game_dec"]

    check_issue(call(command) == 0, "Decryption Failed")

    shutil.copyfile(pboot, src / 'game_dec' / f'ux0_pspemu_temp_game_PSP_GAME_{game_id}' / 'PBOOT.PBP')


def encrypt_game(key, src, dst):
    print("\nEncrypting:\n")
    os.chdir(src)
    if platform.system() == "Linux" or platform.system() == "Darwin":
        os.chmod("./psvimg-create", stat.S_IRWXU)
    command = [str(Path("psvimg-create").absolute()), "-n", "game", "-K", key, "game_dec", str(dst / "game")]

    check_issue(call(command) == 0, "Game Creation Failed")

    shutil.copytree(src / 'license', dst / 'license')
    shutil.copytree(src / 'sce_sys', dst / 'sce_sys')


def make_dir(d):
    try:
        os.makedirs(d, exist_ok=True)
        return Path(d)
    except FileNotFoundError:
        sys.exit("No Working Dir Permissions")


def check_version():
    check_issue(sys.version_info.major == 3 and sys.version_info.minor == 7, "Old Python")


def check_issue(passed: bool, fail_code: str, fatal: bool = True):
    if not passed and fatal:
        sys.exit(fail_code)
    return passed


def pretty_exit_code(code: str):
    switcher = {
        "Apps Path Does Not Exist": "Your appsPath does not exist. Please ensure you have run QCMA and" +
                                    "backed up your game",
        "Old Python": f"FinTrinity requires Python 3.7.3. You have the following version: {sys.version}",
        "QCMA Settings Missing": "QCMA Settings are missing! Please ensure you have QCMA installed",
        "Aborted by User": "You have aborted FinTrinity",
        "No Working Dir Permissions": "FinTrinity cannot find a place to work. If you are on Windows and Controlled " +
                                      "Folder Access is enabled, please consider disabling it while running " +
                                      "FinTrinity.",
        "Hack Too Small": "Application of Trinity appears to have failed for the reasons listed above.",
        "Decryption Failed": "Decryption failed with the above information.",
        "Game Creation Failed": "Game Creation failed with the above information."
    }
    return switcher.get(code, "Something unexpected occurred. Please let me know on the FinTrinity GitHub.")


def read_hkcu(key: str, val: str):
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_READ) as key:
        return winreg.QueryValueEx(key, val)[0]


def read_conf(val: str):
    with open(os.path.expanduser('~/.config/codestation/qcma.conf')) as config:
        for line in config.readlines():
            if line.startswith(val):
                return line.split("=")[1].replace("\n", "")


def read_plist(val: str):
    filename = os.path.expanduser("~/Library/Preferences/com.codestation.qcma.plist")
    plist = plistlib.loads(open(filename, 'rb').read())
    return plist[val]


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
