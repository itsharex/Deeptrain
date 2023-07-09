package app

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
)

type ValidateUserRequest struct {
	Access string `json:"password" required:"true"`
	Token  string `json:"token" required:"true"`
}

func ValidateUserAPI(ctx *gin.Context) {
	var req ValidateUserRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	if req.Access != viper.GetString("allauth.access") || req.Token == "" {
		ctx.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid access password",
		})
		return
	}

	db := utils.GetDBFromContext(ctx)

	token, err := utils.AES256Decrypt(viper.GetString("allauth.aeskey"), req.Token)
	if err != nil {
		ctx.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid token",
		})
	}

	user := auth.ParseToken(ctx, db, token)
	if user == nil {
		ctx.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  "user not found",
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"status":   user.IsActive(db),
		"username": user.Username,
		"id":       user.ID,
	})
}
