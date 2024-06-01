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