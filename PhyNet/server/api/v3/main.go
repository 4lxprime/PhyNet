package main

import (
	"log"

	dbs "github.com/4lxprime/PhyNet/PhyNet/server/api/v3/internal/databases"
	"github.com/4lxprime/PhyNet/PhyNet/server/api/v3/internal/handlers"
	"github.com/fasthttp/router"
	"github.com/valyala/fasthttp"
)

func Secure(next fasthttp.RequestHandler) fasthttp.RequestHandler {
	return func(ctx *fasthttp.RequestCtx) {
		urlKeyBytes := ctx.QueryArgs().Peek("urlkey")

		if string(urlKeyBytes) != "VEIDVOE9oN8O3C4TnU2RIN1O0rF82mU6RuJwHFQ6GH5mF4NQ3pZ8Z6R7A8dL0" {
			ctx.SetStatusCode(404)
			return
		}

		next(ctx)
	}
}

func main() {
	if err := dbs.ConnectPg(); err != nil {
		log.Fatal(err)
	}

	r := router.New()
	v3 := r.Group("/v3")

	v3.GET("/version", func(ctx *fasthttp.RequestCtx) {
		ctx.SetBodyString("latest")
		ctx.SetStatusCode(200)
	})
	v3.GET("/dispatch", handlers.HandleDispatch)
	v3.GET("/login", handlers.HandleLogin)
	v3.GET("/relays_edit", handlers.HandleRelaysEdit)
	v3.GET("/swap_key", handlers.HandleRelaysEdit)
	v3.GET("/get_swap_key", handlers.HandleGetSwapKey)

	if err := fasthttp.ListenAndServe(":8052", Secure(r.Handler)); err != nil {
		log.Fatal(err)
	}
}
