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
	Username string         `form:"username" binding:"required"`
	Password string         `form:"password" binding:"required"`
	Captcha  GeeTestRequest `form:"captcha" binding:"required"`
}

type RegisterForm struct {
	Username   string         `form:"username" binding:"required"`
	Password   string         `form:"password" binding:"required"`
	RePassword string         `form:"re_password" binding:"required"`
	Email      string         `form:"email" binding:"required"`
	Captcha    GeeTestRequest `form:"captcha" binding:"required"`
}

type ResetForm struct {
	Email   string         `form:"email" binding:"required"`
	Captcha GeeTestRequest `form:"captcha" binding:"required"`
}

type VerifyForm struct {
	Code string `form:"code" binding:"required"`
}

func LoginView(c *gin.Context) {
	var form LoginForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}
	username, password := strings.TrimSpace(form.Username), strings.TrimSpace(form.Password)
	if !utils.All(
		ValidateUsername(username),
		ValidatePassword(password),
		GeeTestCaptcha(form.Captcha),
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
	username, password, email := strings.TrimSpace(form.Username), strings.TrimSpace(form.Password), strings.TrimSpace(form.Email)
	if !utils.All(
		ValidateUsername(username),
		ValidatePassword(password),
		ValidateEmail(email),
		GeeTestCaptcha(form.Captcha),
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
	cache.Set(context.Background(), fmt.Sprintf(":mailrate:%s", email), "1", 1*time.Minute)
	go SendVerifyMail(email, code)

	c.JSON(http.StatusOK, gin.H{"status": true, "token": user.GenerateToken()})
}

func ResetView(c *gin.Context) {
	var form ResetForm
	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}
	email := strings.TrimSpace(form.Email)
	if !utils.All(
		ValidateEmail(email),
		GeeTestCaptcha(form.Captcha),
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "We cannot verify your identity. Please check again to verify you are human."})
		return
	}

	if !isEmailExists(db, email) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Email does not exist. Please try another email."})
		return
	}

	code := utils.GenerateChar(12)
	cache.Set(context.Background(), fmt.Sprintf(":reset:%s", email), code, 30*time.Minute)
	cache.Set(context.Background(), fmt.Sprintf(":mailrate:%s", email), "1", 1*time.Minute)

	utils.GetDBFromContext(c).Query("UPDATE auth SET password = ? WHERE email = ?", utils.Sha2Encrypt(code), email)
	go SendResetMail(email, code)

	c.JSON(http.StatusOK, gin.H{"status": true})
}

func VerifyView(c *gin.Context) {
	var form VerifyForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}

	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
	username := c.MustGet("user")
	if username == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not logged in."})
		return
	}
	instance := &User{Username: username.(string)}
	code := cache.Get(c, fmt.Sprintf(":verify:%s", instance.Username))
	if form.Code != code.Val() {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Your verification code is incorrect. Please check again."})
		return
	}

	instance.Activate(db)

	if email, err := instance.GetField(db, "email"); err == nil {
		go SendWelcomeMail(instance.Username, email)
	}
	cache.Del(c, fmt.Sprintf(":verify:%s", instance.Username))
	c.JSON(http.StatusOK, gin.H{"status": true})
}

func ResendView(c *gin.Context) {
	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
	username := c.MustGet("user")
	if username == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not logged in."})
		return
	}

	instance := &User{Username: username.(string)}
	if instance.IsActive(db) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is already activated."})
		return
	}
	email, err := instance.GetField(db, "email")
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Server error. Please try again later or contact admin."})
		return
	}

	rate := cache.Get(c, fmt.Sprintf(":mailrate:%s", email))
	if rate.Val() != "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "You can only resend verification code once per 1 minutes."})
		return
	}
	cache.Set(context.Background(), fmt.Sprintf(":mailrate:%s", email), "1", 1*time.Minute)

	code := utils.GenerateCode(6)
	cache.Set(context.Background(), fmt.Sprintf(":verify:%s", instance.Username), code, 30*time.Minute)

	go SendVerifyMail(email, code)

	c.JSON(http.StatusOK, gin.H{"status": true})
}

func StateView(c *gin.Context) {
	username := c.MustGet("user")
	if username == "" {
		c.JSON(http.StatusOK, gin.H{"status": 0})
		return
	}
	instance := &User{Username: username.(string)}
	if instance.IsActive(utils.GetDBFromContext(c)) {
		c.JSON(http.StatusOK, gin.H{"status": 2})
		return
	}
	c.JSON(http.StatusOK, gin.H{"state": 1})
}

func UserView(c *gin.Context) {
	db := utils.GetDBFromContext(c)
	username := c.Param("username")
	if isUserExists(db, username) {
		user := &User{Username: username}
		if user.IsActive(db) {
			err := db.QueryRow("SELECT is_admin, created_at From auth WHERE username = ?", username).Scan(&user.IsAdmin, &user.CreateAt)
			if err == nil {
				c.JSON(http.StatusOK, gin.H{"status": true, "user": map[string]interface{}{
					"username":   user.Username,
					"created_at": user.CreateAt,
					"is_admin":   user.IsAdmin,
				}})
				return
			}
		}
	}
	c.JSON(http.StatusOK, gin.H{"status": false})
}
