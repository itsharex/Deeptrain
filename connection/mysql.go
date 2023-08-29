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

	// initialize model
	initializeUserModel(DB)
	initializeOAuthModel(DB)
	initializeCertModel(DB)
	initializePackageModel(DB)
	initializePaymentModel(DB)
	initializePaymentLogModel(DB)

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

func initializeOAuthModel(DB *sql.DB) {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS oauth (
		    id INT AUTO_INCREMENT PRIMARY KEY,
		    user_id INT NOT NULL,
		    provider VARCHAR(24) NOT NULL,
		    provider_id VARCHAR(100) NOT NULL,
		    provider_name VARCHAR(100) NOT NULL,
		    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		    FOREIGN KEY (user_id) REFERENCES auth(id)
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
}

func initializeCertModel(DB *sql.DB) {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS cert (
		    id INT AUTO_INCREMENT PRIMARY KEY,
		    user_id INT NOT NULL UNIQUE,
		    verify_id VARCHAR(100) NOT NULL,
		    cert_name VARCHAR(100) NOT NULL,
		    cert_number VARCHAR(480) NOT NULL,
		    cert_type INT NOT NULL DEFAULT 0,
		    cert_status BOOLEAN NOT NULL DEFAULT FALSE,
		    birth_date DATE NOT NULL,
		    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		    FOREIGN KEY (user_id) REFERENCES auth(id)
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
}

func initializePackageModel(DB *sql.DB) {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS package (
		    id INT AUTO_INCREMENT PRIMARY KEY,
		    user_id INT NOT NULL,
		    package_name VARCHAR(100) NOT NULL,
		    package_expire DATE NOT NULL,
		    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		    FOREIGN KEY (user_id) REFERENCES auth(id)
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
}

func initializePaymentModel(DB *sql.DB) {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS payment (
		    id INT AUTO_INCREMENT PRIMARY KEY,
		    user_id INT NOT NULL UNIQUE,
		    amount DECIMAL(10,2) NOT NULL,
		    total_amount DECIMAL(12,2) NOT NULL,
		    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		    FOREIGN KEY (user_id) REFERENCES auth(id)
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
}

func initializePaymentLogModel(DB *sql.DB) {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS payment_log (
		    id INT AUTO_INCREMENT PRIMARY KEY,
		    user_id INT NOT NULL,
		    order_id VARCHAR(100) NOT NULL UNIQUE,
		    amount DECIMAL(10,2) NOT NULL,
		    payment_type VARCHAR(100) NOT NULL,
		    payment_status BOOLEAN NOT NULL DEFAULT FALSE,
		    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		    FOREIGN KEY (user_id) REFERENCES auth(id)
		)
	`)
	if err != nil {
		log.Fatal(err)
	}
}
