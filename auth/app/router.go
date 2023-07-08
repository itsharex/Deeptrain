package app

import "github.com/gin-gonic/gin"

func Register(router *gin.Engine) {
	app := router.Group("/app")
	{
		app.POST("/validate", ValidateUserAPI)
	}
}
