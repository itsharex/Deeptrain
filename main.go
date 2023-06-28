package main

import (
	"deeptrain/auth"
	"deeptrain/connection"
	"deeptrain/middleware"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"log"
)

func main() {
	viper.SetConfigFile("config.yaml")
	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file, %s", err)
	}
	cache := connection.ConnectRedis()
	db := connection.ConnectMySQL()

	if viper.GetBool("debug") {
		gin.SetMode(gin.DebugMode)
	} else {
		gin.SetMode(gin.ReleaseMode)
	}

	app := gin.Default()
	{
		app.Use(middleware.CORSMiddleware())
		app.Use(middleware.DBMiddleWare(db, cache))
		app.Use(middleware.AuthMiddleware())
	}
	{
		app.POST("/login", auth.LoginView)
		app.POST("/register", auth.RegisterView)
		app.POST("/verify", auth.VerifyView)
		app.GET("/state", auth.StateView)
	}

	defer cache.Close()
	defer db.Close()

	if err := app.Run(viper.GetString("server.addr")); err != nil {
		panic(err)
	}
}
