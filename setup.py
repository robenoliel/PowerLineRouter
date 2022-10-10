import os
import subprocess
import sys

def setUpEnv():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pipwin"])
    subprocess.check_call([sys.executable, "-m", "pipwin", "install", 'gdal'])
    subprocess.check_call([sys.executable, "-m", "pipwin", "install", 'fiona'])

if __name__ == "__main__":
    setUpEnv()