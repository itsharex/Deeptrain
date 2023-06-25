package main

import (
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"log"
)

func main() {
	viper.SetConfigFile("config.yaml")
	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file, %s", err)
	}

	app := gin.Default()

	if err := app.Run(viper.GetString("addr")); err != nil {
		panic(err)
	}
}
