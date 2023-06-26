package auth

import (
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

type LoginForm struct {
	Username string `form:"username" binding:"required"`
	Password string `form:"password" binding:"required"`
	Captcha  string `form:"captcha" binding:"required"`
}

type RegisterForm struct {
	Username   string `form:"username" binding:"required"`
	Password   string `form:"password" binding:"required"`
	RePassword string `form:"re_password" binding:"required"`
	Email      string `form:"email" binding:"required"`
	Captcha    string `form:"captcha" binding:"required"`
}

func LoginView(c *gin.Context) {
	var form LoginForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}
	username, password, captcha := strings.TrimSpace(form.Username), strings.TrimSpace(form.Password), strings.TrimSpace(form.Captcha)
	if !utils.All(
		ValidateUsername(username),
		ValidatePassword(password),
		LoginCaptcha(captcha) >= 0.8,
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "We cannot verify your identity. Please check again to verify you are human."})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": true})
}

func RegisterView(c *gin.Context) {
	var form RegisterForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}
	username, password, email, captcha := strings.TrimSpace(form.Username), strings.TrimSpace(form.Password), strings.TrimSpace(form.Email), strings.TrimSpace(form.Captcha)
	if !utils.All(
		ValidateUsername(username),
		ValidatePassword(password),
		ValidateEmail(email),
		RegisterCaptcha(captcha) >= 0.8,
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "We cannot verify your identity. Please check again to verify you are human."})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": true})
}
