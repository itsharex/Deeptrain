package pay

import "github.com/gin-gonic/gin"

func Register(app *gin.Engine) {
	app.GET("/cert/refresh", RefreshCertView)
	app.POST("/cert/request", RequestCertView)
	app.GET("/cert/state", GetCertStateView)
	app.GET("/cert/qrcode", GetCertQRCodeView)

	app.POST("/pay/create", CreatePaymentView)
	app.GET("/pay/log", GetPaymentLogView)
	app.GET("/pay/amount", GetAmountView)
	app.GET("/pay/trade", GetTradeStatusView)

	app.POST("/pay/alipay/notify", VerifyAliPayReturn)
}
