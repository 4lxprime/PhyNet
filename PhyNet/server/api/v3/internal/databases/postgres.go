package databases

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

var postgres *sql.DB = nil

func ConnectPg() error {
	pgURI := "localhost"
	pgUser := "root"
	pgPassword := "toor"

	if pgURI == "" || pgUser == "" || pgPassword == "" {
		return fmt.Errorf("missing Postgres datas")
	}

	connStr := fmt.Sprintf("postgres://%s:%s@%s?sslmode=disable", pgUser, pgPassword, pgURI)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return err
	}

	if err = db.Ping(); err != nil {
		return err
	}

	postgres = db

	return nil
}

func GetPostgres() *sql.DB {
	return postgres
}
