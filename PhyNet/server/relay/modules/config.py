from dataclasses import dataclass
from typing import ClassVar
from socket import socket as Sock
from cryptography.fernet import Fernet
from colorama import Fore

@dataclass
class c2_config_time:
    GETBOT: ClassVar[int] = 120
    NET: ClassVar[int] = 240
    PING: ClassVar[int] = 30
    UPTITLE: ClassVar[int] = 1

@dataclass
class c2_config_addr:
    CNC_IP: ClassVar[str] = "127.0.0.1"
    CNC_PORT: ClassVar[int] = 8080
    CNC_ADDR: ClassVar[tuple[str, int]] = (CNC_IP, CNC_PORT)

@dataclass
class relay_config_time:
    PING: ClassVar[int] = 30
    NET: ClassVar[int] = 500
    GENKEY: ClassVar[int] = 30 #1800
    SAVE: ClassVar[int] = 1000
    RELAY: ClassVar[int] = 30

@dataclass
class relay_config_addr:
    RELAY_IP: ClassVar[str] = "127.0.0.1"
    RELAY_PORT: ClassVar[int] = 5000
    RELAY_ADDR: ClassVar[tuple[str, int]] = (RELAY_IP, RELAY_PORT)

@dataclass
class RelayConfig:
    # constants
    URL_KEY: ClassVar[str] = "VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0"
    RELAY_KEY: ClassVar[str] = "gAAAAABi2DQ2aBL7F1w-YK7tJQwZb_lnZY099Q2iCXqcLbLZy75ULiQk_VYWFglVco5PJrr0X-Jov_OaGwmL5HL5oYGqpACT7IiGspfgByyXQgY6U5an0Hk="
    ENC_KEY: ClassVar[str] = "kg6QH9EBtZUziQ8DdEqwnCknt7lKTfpc2zEEvb3Imms="
    PASSWD: ClassVar[str] = "gAAAAABixrd26TgeuuQmRhjWorB1oea-lO950B8hWYNHSTL2NvA3RW7A9MWAJXmDOeTJW9z5AWMp2pR0GHZqGPG36W2tXqPpLWkunwvc4CV8z5eJ0LNk5BU="
    API_URL: ClassVar[str] = "http://127.0.0.1:8052/v3"

    debug: bool
    fernet: Fernet
    bot_speed: int # actual netspeed of all bot
    bots_sock: dict[Sock, tuple[str, int]] # number of bots
    swap_key: str
    swap_key_old: str

    # config elements
    cnc_addr: c2_config_addr
    cnc_time: c2_config_time
    relay_addr: relay_config_addr
    relay_time: relay_config_time

    # colors things here
    ANSI_CLEAR: ClassVar[str] = '\033[2J\033[H'
    COLOR_GREEN: ClassVar[str] = Fore.GREEN
    COLOR_WHITE: ClassVar[str] = Fore.WHITE
    COLOR_RESET: ClassVar[str] = Fore.RESET
    COLOR_RED: ClassVar[str] = Fore.RED

    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        self.fernet = Fernet(self.ENC_KEY)
        self.bots_sock = {}
        self.bot_speed = 0
        self.swap_key = None
        self.swap_key_old = None

        self.cnc_addr = c2_config_addr()
        self.cnc_time = c2_config_time()
        self.relay_addr = relay_config_addr()
        self.relay_time = relay_config_time()
