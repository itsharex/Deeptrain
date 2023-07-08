package connection

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/spf13/viper"
	"log"
)

var _ *sql.DB

func ConnectMySQL() *sql.DB {
	// connect to MySQL
	DB, err := sql.Open("mysql", fmt.Sprintf(
		"%s:%s@tcp(%s:%d)/%s",
		viper.GetString("mysql.user"),
		viper.GetString("mysql.password"),
		viper.GetString("mysql.host"),
		viper.GetInt("mysql.port"),
		viper.GetString("mysql.db"),
	))
	if err != nil {
		log.Fatalln("Failed to connect to MySQL server: ", err)
	} else {
		log.Println("Connected to MySQL server successfully")
	}

	// initialize user model
	initializeUserModel(DB)

	return DB
}

func initializeUserModel(DB *sql.DB) {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS auth (
		    id INT AUTO_INCREMENT PRIMARY KEY,
			username VARCHAR(24) UNIQUE,
			password VARCHAR(64) NOT NULL,
			email VARCHAR(100) NOT NULL,
		    active BOOLEAN NOT NULL DEFAULT FALSE,
		    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		    is_admin BOOLEAN NOT NULL DEFAULT FALSE
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
}
