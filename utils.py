import os
import shutil
import errno
import winreg


def make_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def make_copy(src, dst):
    if not os.path.exists(dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                raise


def read_hkcu(key: str, val: str):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_READ) as key:
        return winreg.QueryValueEx(key, val)[0]
