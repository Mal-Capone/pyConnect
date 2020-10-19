from pyCon.client import PyConClient as client
from pyCon.server import PyConServer as server
from pathlib import Path



def setup_download_dir():
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir

if __name__ == '__main__':
    while True:
        print("Welcome")

