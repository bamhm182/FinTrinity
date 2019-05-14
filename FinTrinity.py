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
            if platform.uname().system == "Windows":
                self.apps_path = Path(Utils.read_hkcu(r"Software\codestation\qcma", 'appsPath')) / 'PGAME'
                account = Utils.read_hkcu(r"Software\codestation\qcma", 'lastAccountId')
                username = Utils.read_hkcu(r"Software\codestation\qcma", 'lastOnlineId')
            elif platform.uname().system == "Linux":
                self.apps_path = Path(Utils.read_conf('Linux', 'appsPath'))
                account = Utils.read_conf('Linux', 'lastAccountId')
                username = Utils.read_conf('Linux', 'lastOnlineId')

            if not os.path.exists(self.apps_path):
                print(f"{self.apps_path} does not exist. Please ensure you have run QCMA and backed up your game.")
                sys.exit("Apps Path Does Not Exist")

            if username and account:
                self.user.set_id(account)
                self.user.set_name(username)
                self.user.set_path(self.apps_path)
                self.game = self.user.games[0]
        except FileNotFoundError:
            print("QCMA registry keys do not exist! Please ensure you have run QCMA and backed up your game.")
            sys.exit("QCMA Registry Keys Missing")

    def confirm_find(self):
        ans = input(
            f"{self.game.title} ({self.game.id}) found for {self.user.name} ({self.user.id}). Continue? (yes/no): ")
        if ans[0] != "y" and ans[0] != "Y":
            sys.exit("Aborted by User")

    def setup_dirs(self):
        base_dir = "C:"
        if os.access(Utils.get_home() / 'Desktop', os.W_OK):
            base_dir = Utils.get_home() / 'Desktop'
        elif not os.access(base_dir, os.W_OK):
            print(r"Cannot write to either your Desktop or C:\ for some reason")
            sys.exit("No Working Dir Permissions")

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
        Utils.download('https://github.com/TheOfficialFloW/Trinity/releases/download/v1.0/PBOOT.PBP', self.working_dir)
        Utils.download('https://github.com/yifanlu/psvimgtools/releases/download/v0.1/psvimgtools-0.1-win64.zip',
                       self.working_dir)
        Utils.extract(self.working_dir / 'psvimgtools-0.1-win64.zip', self.decrypt_dir)

    def hack(self):
        print(f"Applying Trinity Hack:\n\n\n")
        Utils.decrypt_game(self.user.decrypt_key, self.decrypt_dir, self.working_dir / "PBOOT.PBP", self.game.id)
        Utils.encrypt_game(self.user.decrypt_key, self.decrypt_dir, self.hack_dir)

        if os.path.getsize(self.hack_dir / 'game' / 'game.psvimg') < 1000000:
            print('Application of Trinity appears to have failed for the reasons listed above.')
            sys.exit('Hack Too Small')

        Utils.replace_folder(self.hack_dir, self.game.path)
        print(f"\n\n\nTrinity Applied. Please refresh your QCMA database and transfer your game back to your Vita.")


if __name__ == "__main__":
    try:
        fin = FinTrinity()
        fin.read_config()
        fin.confirm_find()
        fin.setup_dirs()
        fin.backup_game()
        fin.download_dependencies()
        fin.hack()
    except SystemExit:
        pass
    finally:
        input("[PRESS ENTER TO CLOSE]")
