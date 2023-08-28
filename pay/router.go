package pay

import "github.com/gin-gonic/gin"

func Register(app *gin.Engine) {
	app.GET("/cert/refresh", RefreshCertView)
	app.POST("/cert/request", RequestCertView)
	app.GET("/cert/state", GetCertStateView)
}
