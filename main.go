package main

import (
	"deeptrain/auth"
	"deeptrain/middleware"
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"log"
)

func main() {
	viper.SetConfigFile("config.yaml")
	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file, %s", err)
	}
	rdb := utils.ConnectRedis()
	db := utils.ConnectMySQL()

	app := gin.Default()
	{
		app.Use(middleware.CORSMiddleware())
	}
	{
		app.POST("/login", auth.LoginView)
	}

	defer rdb.Close()
	defer db.Close()

	if err := app.Run(viper.GetString("server.addr")); err != nil {
		panic(err)
	}
}
