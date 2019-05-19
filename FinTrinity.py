import sys
import os
import shutil
import platform
from pathlib import Path
from classes import Utils
from classes.User import User
from classes.Game import Game


class FinTrinity:
    def __init__(self):
        self.apps_path = ""
        self.working_dir = ""
        self.hack_dir = ""
        self.decrypt_dir = ""
        self.backup_dir = ""
        self.user = User()
        self.game = Game()

    def read_config(self):
        try:
            username = None
            account = None

            if platform.system() == "Windows":
                self.apps_path = Path(Utils.read_hkcu(r"Software\codestation\qcma", 'appsPath')) / 'PGAME'
                account = Utils.read_hkcu(r"Software\codestation\qcma", 'lastAccountId')
                username = Utils.read_hkcu(r"Software\codestation\qcma", 'lastOnlineId')
            elif platform.system() == "Linux":
                self.apps_path = Path(Utils.read_conf('appsPath')) / 'PGAME'
                account = Utils.read_conf('lastAccountId')
                username = Utils.read_conf('lastOnlineId')
            elif platform.system() == "Darwin":
                self.apps_path = Path(Utils.read_plist('appsPath')) / 'PGAME'
                account = Utils.read_plist('lastAccountId')
                username = Utils.read_plist('lastOnlineId')

            Utils.check_issue(os.path.exists(self.apps_path), "Apps Path Does Not Exist")

            if username and account:
                self.user.set_id(account)
                self.user.set_name(username)
                self.user.set_path(self.apps_path)
                self.game = self.user.games[0]
        except FileNotFoundError:
            sys.exit("QCMA Settings Missing")

    def confirm_find(self):
        ans = input(
            f"{self.game.title} ({self.game.id}) found for {self.user.name} ({self.user.id}). Continue? (yes/no): ")
        Utils.check_issue(ans[0] in "yY", "Aborted by User")

    def setup_dirs(self):
        base_dir = "C:"

        if Utils.check_issue(os.access(Utils.get_home() / 'Desktop', os.W_OK), "No Working Dir Permissions", False):
            base_dir = Utils.get_home() / 'Desktop'

        Utils.check_issue(os.access(base_dir, os.W_OK), "No Working Dir Permissions")

        self.working_dir = Utils.make_dir(base_dir / f"FinTrinity{Utils.get_timestamp()}")
        self.hack_dir = Utils.make_dir(self.working_dir / f"{self.game.id}.hacked")
        self.decrypt_dir = self.working_dir / f"{self.game.id}.decrypted"
        self.backup_dir = self.working_dir / f"{self.game.id}.backup"
        print(f"Created Working Directory: {self.working_dir}")

    def backup_game(self):
        shutil.copytree(self.game.path, self.backup_dir)
        shutil.copytree(self.game.path, self.decrypt_dir)

    def download_dependencies(self):
        print(f"Downloading and Extracting Dependencies")
        psvimgtools = None
        if platform.system() == "Windows":
            if platform.machine() == "AMD64":
                psvimgtools = "https://github.com/yifanlu/psvimgtools/releases/download/v0.1/psvimgtools-0.1-win64.zip"
            else:
                psvimgtools = "https://github.com/yifanlu/psvimgtools/releases/download/v0.1/psvimgtools-0.1-win32.zip"
        elif platform.system() == "Linux":
            psvimgtools = "https://github.com/yifanlu/psvimgtools/releases/download/v0.1/psvimgtools-0.1-linux64.zip"
        elif platform.system() == "Darwin":
            psvimgtools = "https://github.com/yifanlu/psvimgtools/releases/download/v0.1/psvimgtools-0.1-osx.zip"

        Utils.download('https://github.com/TheOfficialFloW/Trinity/releases/download/v1.0/PBOOT.PBP', self.working_dir)
        Utils.download(psvimgtools, self.working_dir)
        Utils.extract(self.working_dir / psvimgtools.split("/")[-1], self.decrypt_dir)

    def hack(self):
        print(f"Applying Trinity Hack:\n\n\n")
        Utils.decrypt_game(self.user.decrypt_key, self.decrypt_dir, self.working_dir / "PBOOT.PBP", self.game.id)
        Utils.encrypt_game(self.user.decrypt_key, self.decrypt_dir, self.hack_dir)

        Utils.check_issue(os.path.getsize(self.hack_dir / 'game' / 'game.psvimg') > 1000000, "Hack Too Small")

        Utils.replace_folder(self.hack_dir, self.game.path)
        print(f"\n\n\nTrinity Applied. Please refresh your QCMA database and transfer your game back to your Vita.")


if __name__ == "__main__":
    try:
        Utils.check_version()
        fin = FinTrinity()
        fin.read_config()
        fin.confirm_find()
        fin.setup_dirs()
        fin.backup_game()
        fin.download_dependencies()
        fin.hack()
    except SystemExit as e:
        print(Utils.pretty_exit_code(e.code))
        pass
    finally:
        input("[PRESS ENTER TO CLOSE]")
