package auth

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type LoginForm struct {
	User     string `form:"user" binding:"required"`
	Password string `form:"password" binding:"required"`
	Captcha  string `form:"captcha" binding:"required"`
}

func LoginView(c *gin.Context) {
	var form LoginForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"status": "bad request"})
		return
	}
	if !(ValidateUsername(form.User) && ValidatePassword(form.Password)) {
		c.JSON(http.StatusBadRequest, gin.H{"status": "bad request"})
	}

	score := Login(form.Captcha)
	c.JSON(http.StatusOK, gin.H{"status": "ok", "score": score})
}
