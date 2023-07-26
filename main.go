package main

import (
	"deeptrain/auth"
	oauth "deeptrain/auth/app"
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
		app.Use(middleware.ThrottleMiddleware())
	}
	{
		app.POST("/login", auth.LoginView)
		app.POST("/register", auth.RegisterView)
		app.POST("/reset", auth.ResetView)
		app.POST("/verify", auth.VerifyView)
		app.POST("/resend", auth.ResendView)
		app.GET("/state", auth.StateView)
		app.GET("/info", auth.InfoView)
		app.POST("/settings/password", auth.ChangePasswordView)
		app.POST("/settings/email", auth.ChangeEmailView)
		app.POST("/settings/verify", auth.ChangeEmailVerifyView)
		app.GET("/user/:username", auth.UserView)

		oauth.Register(app)
	}

	defer cache.Close()
	defer db.Close()

	if err := app.Run(viper.GetString("server.addr")); err != nil {
		panic(err)
	}
}
