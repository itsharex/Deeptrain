package main

import (
	"deeptrain/auth"
	allauth "deeptrain/auth/app"
	"deeptrain/auth/oauth"
	"deeptrain/connection"
	"deeptrain/middleware"
	"deeptrain/pay"
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

	pay.InitPaymentClient()

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
		app.POST("/mail/send", auth.EmailLoginView)
		app.POST("/mail/verify", auth.EmailLoginVerifyView)
		app.POST("/2fa/verify", auth.Verify2FAView)
		app.GET("/2fa/enable", auth.Enable2FAView)
		app.GET("/2fa/disable", auth.Disable2FAView)
		app.GET("/2fa/activate", auth.Activate2FAView)
		app.POST("/settings/password", auth.ChangePasswordView)
		app.POST("/settings/email", auth.ChangeEmailView)
		app.POST("/settings/verify", auth.ChangeEmailVerifyView)
		app.GET("/user/:username", auth.UserView)
		app.GET("/avatar/:username", auth.GetAvatarView)
		app.POST("/avatar", auth.PostAvatarView)
		app.GET("/package/state", auth.PackageView)

		pay.Register(app)
		oauth.Register(app)
		allauth.Register(app)
	}

	defer cache.Close()
	defer db.Close()

	if err := app.Run(viper.GetString("server.addr")); err != nil {
		panic(err)
	}
}
