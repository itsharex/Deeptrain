package app

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
)

type PaymentRequest struct {
	Access string `json:"password" required:"true"`
	User   string `json:"user" required:"true"`
	Hash   string `json:"hash" required:"true"`
	Order  string `json:"order" required:"true"`
	Sign   string `json:"sign" required:"true"`
}

type CreatePaymentRequest struct {
	Access string  `json:"password" required:"true"`
	User   string  `json:"user" required:"true"`
	Amount float32 `json:"amount" required:"true"`
	Hash   string  `json:"hash" required:"true"`
	Sign   string  `json:"sign" required:"true"`
	Order  string  `json:"order" required:"true"`
}

func GetUserPaymentAPI(c *gin.Context) {
	var req PaymentRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	if req.Access != viper.GetString("allauth.access") ||
		!utils.Sha2Compare(req.User+viper.GetString("allauth.salt"), req.Hash) ||
		!utils.Sha2Compare(req.User+req.Order+viper.GetString("allauth.sign"), req.Sign) {
		c.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid access password",
		})
		return
	}

	db := utils.GetDBFromContext(c)

	user := auth.User{
		Username: req.User,
	}

	c.JSON(http.StatusOK, gin.H{
		"status":  true,
		"balance": user.GetBalance(db),
	})
}

func CreatePaymentAPI(c *gin.Context) {
	var req CreatePaymentRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	if req.Access != viper.GetString("allauth.access") ||
		!utils.Sha2Compare(req.User+viper.GetString("allauth.salt"), req.Hash) ||
		!utils.Sha2Compare(req.User+req.Order+viper.GetString("allauth.sign"), req.Sign) {
		c.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid access password",
		})
		return
	}

	db := utils.GetDBFromContext(c)

	user := auth.User{
		Username: req.User,
	}

	c.JSON(http.StatusOK, gin.H{
		"status": true,
		"type":   user.Pay(db, req.Amount),
	})
}
