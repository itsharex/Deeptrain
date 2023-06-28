package auth

import (
	"context"
	"deeptrain/utils"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
	"time"
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

	if !ValidateUser(utils.GetDBFromContext(c), username, password) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Username or password is incorrect."})
		return
	}

	user := User{Username: username, Password: password}
	c.JSON(http.StatusOK, gin.H{"status": true, "token": user.GenerateToken()})
}

func RegisterView(c *gin.Context) {
	var form RegisterForm
	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
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

	if isUserExists(db, username) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User already exists. Please try another username."})
		return
	}
	if isEmailExists(db, email) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Email already exists. Please try another email."})
		return
	}
	user := User{
		Username: username,
		Password: utils.Sha2Encrypt(password),
		Email:    email,
		Active:   false,
		IsAdmin:  false,
	}
	if !user.Save(db) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Server error. Please try again later or contact admin."})
		return
	}

	code := utils.GenerateCode(6)
	cache.Set(context.Background(), fmt.Sprintf(":verify:%s", username), code, 30*time.Minute)
	go SendVerifyMail(email, code)

	c.JSON(http.StatusOK, gin.H{"status": true, "token": user.GenerateToken()})
}

func VerifyView(c *gin.Context) {
	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
	user := c.MustGet("user")
	if user == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not logged in."})
		return
	}
	instance := user.(*User)
	fmt.Println(instance.Username)
	code := cache.Get(c, fmt.Sprintf(":verify:%s", instance.Username))
	if c.Query("code") != code.Val() {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Your verification code is incorrect. Please check again."})
		return
	}

	instance.Activate(db)

	if email, err := instance.GetField(db, "email"); err != nil {
		go SendWelcomeMail(instance.Username, email)
	}
	c.JSON(http.StatusOK, gin.H{"status": true})
}
