package app

import "github.com/gin-gonic/gin"

func Register(router *gin.Engine) {
	app := router.Group("/app")
	{
		app.POST("/validate", ValidateUserAPI)
		app.POST("/email", EmailAPI)
		app.POST("/cert", CertAPI)
		app.POST("/balance", GetUserPaymentAPI)
		app.POST("/payment", CreatePaymentAPI)
	}
}
