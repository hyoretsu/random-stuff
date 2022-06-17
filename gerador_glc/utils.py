import os
import subprocess
import sys


def clear():
    os.system("cls||clear")


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
