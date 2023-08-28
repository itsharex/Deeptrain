package app

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
)

type ValidateUserRequest struct {
	Access string `json:"password" required:"true"`
	Token  string `json:"token" required:"true"`
	Hash   string `json:"hash" required:"true"`
}

type EmailRequest struct {
	Access  string `json:"password" required:"true"`
	User    string `json:"user" required:"true"`
	Hash    string `json:"hash" required:"true"`
	Subject string `json:"subject" required:"true"`
	Body    string `json:"body" required:"true"`
}

type CertRequest struct {
	Access string `json:"password" required:"true"`
	User   string `json:"user" required:"true"`
	Hash   string `json:"hash" required:"true"`
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

	if req.Access != viper.GetString("allauth.access") || !utils.Sha2Compare(req.Token+viper.GetString("allauth.salt"), req.Hash) {
		ctx.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid access password",
		})
		return
	}

	db := utils.GetDBFromContext(ctx)

	user := auth.ParseToken(ctx, db, req.Token)
	if user == nil {
		ctx.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  "user not found",
		})
		return
	}

	var id int64
	_ = db.QueryRow("SELECT id FROM auth WHERE username = ?", user.Username).Scan(&id)
	ctx.JSON(http.StatusOK, gin.H{
		"status":   user.IsActive(db),
		"username": user.Username,
		"id":       id,
	})
}

func EmailAPI(ctx *gin.Context) {
	var req EmailRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	if req.Access != viper.GetString("allauth.access") || !utils.Sha2Compare(req.User+viper.GetString("allauth.salt"), req.Hash) {
		ctx.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid access password",
		})
		return
	}

	if req.Subject == "" || req.Body == "" {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"status": false,
			"error":  "subject or body is empty",
		})
		return
	}

	db := utils.GetDBFromContext(ctx)

	var email string
	if err := db.QueryRow("SELECT email FROM auth WHERE username = ?", req.User).Scan(&email); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  fmt.Sprintf("user %s not found", req.User),
		})
		return
	}

	utils.SendMail(email, req.Subject, req.Body)

	ctx.JSON(http.StatusOK, gin.H{
		"status": true,
		"user":   req.User,
		"email":  email,
	})
}

func CertAPI(ctx *gin.Context) {
	var req CertRequest
	if err := ctx.ShouldBindJSON(&req); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	if req.Access != viper.GetString("allauth.access") || !utils.Sha2Compare(req.User+viper.GetString("allauth.salt"), req.Hash) {
		ctx.JSON(http.StatusUnauthorized, gin.H{
			"status": false,
			"error":  "invalid access password",
		})
		return
	}

	db := utils.GetDBFromContext(ctx)
	user := auth.User{
		Username: req.User,
	}

	ctx.JSON(http.StatusOK, gin.H{
		"status": true,
		"cert":   user.IsCert(db, ctx),
	})
}
