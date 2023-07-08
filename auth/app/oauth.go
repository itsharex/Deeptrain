package app

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
	"strings"
)

func ValidateUserAPI(ctx *gin.Context) {
	password := ctx.PostForm("password")
	raw := strings.TrimSpace(ctx.PostForm("token"))

	if password != viper.GetString("allauth.access") || raw == "" {
		ctx.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid access password",
		})
		return
	}

	db := utils.GetDBFromContext(ctx)

	token, err := utils.AES256Decrypt(raw, viper.GetString("allauth.secret"))
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
