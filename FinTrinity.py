import sys
import shutil
import Utils
from User import User
from Game import Game

try:
    apps_path = Utils.read_hkcu(r"Software\codestation\qcma", 'appsPath') + '/PGAME'
    account = Utils.read_hkcu(r"Software\codestation\qcma", 'lastAccountId')
    username = Utils.read_hkcu(r"Software\codestation\qcma", 'lastOnlineId')
    user = User()
    game = Game()

    if username and account:
        user.set_id(account)
        user.set_name(username)
        user.set_path(apps_path)
        game = user.games[0]

    if input(f"{game.title} ({game.id}) found for {user.name} ({user.id}). Continue? (yes/no): ")[0] != "y":
        sys.exit("Aborted by User")

    working_dir = Utils.make_dir(f"{Utils.get_home()}/Desktop/FinTrinity{Utils.get_timestamp()}")
    hack_dir = Utils.make_dir(working_dir / f"{game.id}.hacked")
    decrypt_dir = working_dir / f"{game.id}.decrypted"
    backup_dir = working_dir / f"{game.id}.backup"
    print(f"Created Working Directory: {working_dir}")

    # Backup Game
    shutil.copytree(game.path, backup_dir)
    shutil.copytree(game.path, decrypt_dir)

    # Download Dependencies
    print(f"Downloading and Extracting Dependencies")
    Utils.download('https://github.com/TheOfficialFloW/Trinity/releases/download/v1.0/PBOOT.PBP', working_dir)
    Utils.download('https://github.com/yifanlu/psvimgtools/releases/download/v0.1/psvimgtools-0.1-win64.zip',
                   working_dir)
    Utils.extract(f'{working_dir}/psvimgtools-0.1-win64.zip', decrypt_dir)

    # Hack
    print(f"Applying Trinity Hack:\n\n\n")
    Utils.decrypt_game(user.decrypt_key, decrypt_dir, working_dir / "PBOOT.PBP", game.id)
    Utils.encrypt_game(user.decrypt_key, decrypt_dir, hack_dir)
    Utils.replace_folder(hack_dir, game.path)

    print(f"\n\n\nTrinity Applied. Please refresh your QCMA database and transfer your game back to your Vita.")
except SystemExit:
    pass
finally:
    input("[PRESS ENTER TO CLOSE]")
