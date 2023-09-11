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

type EmailLoginForm struct {
	Email   string         `form:"email" binding:"required"`
	Captcha GeeTestRequest `form:"captcha" binding:"required"`
}

type EmailLoginVerifyForm struct {
	Email string `form:"email" binding:"required"`
	Key   string `form:"key" binding:"required"`
	Code  string `form:"code" binding:"required"`
}

type RegisterForm struct {
	Username   string         `form:"username" binding:"required"`
	Password   string         `form:"password" binding:"required"`
	RePassword string         `form:"re_password" binding:"required"`
	Email      string         `form:"email" binding:"required"`
	Captcha    GeeTestRequest `form:"captcha" binding:"required"`
}

type ResetForm struct {
	Email string `form:"email" binding:"required"`
	Key   string `form:"key" binding:"required"`
	Code  string `form:"code" binding:"required"`
}

type VerifyForm struct {
	Code string `form:"code" binding:"required"`
}

type ChangePasswordForm struct {
	Old     string         `form:"old" binding:"required"`
	New     string         `form:"new" binding:"required"`
	Captcha GeeTestRequest `form:"captcha" binding:"required"`
}

type ChangeEmailForm struct {
	Email   string         `form:"email" binding:"required"`
	Captcha GeeTestRequest `form:"captcha" binding:"required"`
}

type ChangeEmailVerifyForm struct {
	Old string `form:"old" binding:"required"`
	New string `form:"new" binding:"required"`
}

func LoginView(c *gin.Context) {
	var form LoginForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}
	username, password := strings.TrimSpace(form.Username), strings.TrimSpace(form.Password)
	if !utils.All(
		len(username) > 0,
		ValidatePassword(password),
		GeeTestCaptcha(form.Captcha),
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "We cannot verify your identity. Please check again to verify you are human."})
		return
	}

	db := utils.GetDBFromContext(c)
	user := LoginByEmailOrUsername(c, db, username, password)

	if user == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Username or password is incorrect."})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": true, "token": user.GenerateToken()})
}

func EmailLoginView(c *gin.Context) {
	var form EmailLoginForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}

	email, captcha := strings.TrimSpace(form.Email), form.Captcha
	if !utils.All(
		ValidateEmail(email),
		GeeTestCaptcha(captcha),
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "We cannot verify your identity. Please check again to verify you are human."})
		return
	}

	db := utils.GetDBFromContext(c)
	if !IsEmailExists(db, email) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Email does not exist. Please try another email."})
		return
	}

	cache := utils.GetCacheFromContext(c)
	if rate := cache.Get(c, fmt.Sprintf(":mailrate:%s", email)); rate.Val() != "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "You can only login once per 1 minutes."})
		return
	}

	code := utils.GenerateCode(6)
	key := utils.GenerateChar(128)
	go SendVerifyMail(email, code)
	cache.Set(context.Background(), fmt.Sprintf(":mailotp:%s:%s", key, email), code, 5*time.Minute)
	cache.Set(context.Background(), fmt.Sprintf(":mailrate:%s", email), "1", 1*time.Minute)

	c.JSON(http.StatusOK, gin.H{"status": true, "key": key})
}

func EmailLoginVerifyView(c *gin.Context) {
	var form EmailLoginVerifyForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}

	key, code, email := form.Key, form.Code, strings.TrimSpace(form.Email)

	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)

	if code != cache.Get(c, fmt.Sprintf(":mailotp:%s:%s", key, email)).Val() {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Your verification code is incorrect. Please check again."})
		return
	}

	user := GetUserFromEmail(db, email)
	cache.Del(c, fmt.Sprintf(":mailotp:%s:%s", key, email))

	c.JSON(http.StatusOK, gin.H{"status": true, "token": user.GenerateToken(), "username": user.Username})
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

	if IsUserExists(db, username) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User already exists. Please try another username."})
		return
	}
	if IsEmailExists(db, email) {
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
	go SaveAvatar(username)

	c.JSON(http.StatusOK, gin.H{"status": true, "token": user.GenerateToken()})
}

func ResetView(c *gin.Context) {
	var form ResetForm
	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again."})
		return
	}
	email, key, code := strings.TrimSpace(form.Email), strings.TrimSpace(form.Key), strings.TrimSpace(form.Code)

	if !utils.All(
		key != "",
		code != "",
		ValidateEmail(email),
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "We cannot verify your identity. Please check again to verify you are human."})
		return
	}

	if code != cache.Get(c, fmt.Sprintf(":mailotp:%s:%s", key, email)).Val() {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Your verification code is incorrect. Please check again."})
		return
	}

	cache.Del(c, fmt.Sprintf(":mailotp:%s:%s", key, email))

	if !IsEmailExists(db, email) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Email does not exist. Please try another email."})
		return
	}

	char := utils.GenerateChar(12)
	password := utils.Sha2Encrypt(char)

	user := GetUserFromEmail(db, email)
	_, err := db.Query("UPDATE auth SET password = ? WHERE email = ?", password, email)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Server error. Please try again later or contact admin."})
		return
	}

	cache.Set(c, fmt.Sprintf(":validate:%s", user.Username), password, 30*time.Minute)
	go SendResetMail(email, char)

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
		c.JSON(http.StatusOK, gin.H{"status": 0, "username": username})
		return
	}
	instance := &User{Username: username.(string)}
	if instance.IsActive(utils.GetDBFromContext(c)) {
		c.JSON(http.StatusOK, gin.H{"status": 2, "username": username})
		return
	}
	c.JSON(http.StatusOK, gin.H{"status": 1, "username": username})
}

func InfoView(c *gin.Context) {
	username := c.MustGet("user")
	if username == "" {
		c.JSON(http.StatusOK, gin.H{"status": false})
		return
	}
	instance := &User{Username: username.(string)}
	if !instance.IsActive(utils.GetDBFromContext(c)) {
		c.JSON(http.StatusOK, gin.H{"status": false})
		return
	}

	var id int64
	var email string
	var isAdmin bool
	var createdAt []uint8
	err := utils.GetDBFromContext(c).QueryRow("SELECT id, email, is_admin, created_at FROM auth WHERE username = ?", instance.Username).Scan(&id, &email, &isAdmin, &createdAt)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"status":     true,
		"username":   instance.Username,
		"id":         id,
		"email":      email,
		"is_admin":   isAdmin,
		"created_at": utils.ConvertTime(createdAt),
	})
}

func UserView(c *gin.Context) {
	db := utils.GetDBFromContext(c)
	username := c.Param("username")
	if IsUserExists(db, username) {
		user := &User{Username: username}
		if user.IsActive(db) {
			err := db.QueryRow("SELECT is_admin, created_at FROM auth WHERE username = ?", username).Scan(&user.IsAdmin, &user.CreateAt)
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

func ChangePasswordView(c *gin.Context) {
	username := c.MustGet("user")
	if username == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not logged in."})
		return
	}

	var form ChangePasswordForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again.", "message": err.Error()})
		return
	}
	oldPassword, newPassword := strings.TrimSpace(form.Old), strings.TrimSpace(form.New)
	if !utils.All(
		ValidatePassword(oldPassword),
		ValidatePassword(newPassword),
		GeeTestCaptcha(form.Captcha),
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Password is not valid. Please check again."})
		return
	}

	db := utils.GetDBFromContext(c)
	instance := &User{Username: username.(string), Password: utils.Sha2Encrypt(oldPassword)}
	if !instance.Validate(db, c) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Old password is incorrect."})
		return
	}

	if oldPassword == newPassword {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "New password cannot be the same as old password."})
		return
	}

	instance.Password = utils.Sha2Encrypt(newPassword)
	_, err := db.Query("UPDATE auth SET password = ? WHERE username = ?", instance.Password, instance.Username)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Server error. Please try again later.", "message": err.Error()})
		return
	}

	cache := utils.GetCacheFromContext(c)
	cache.Set(c, fmt.Sprintf(":validate:%s", instance.Username), instance.Password, 30*time.Minute)
	c.JSON(http.StatusOK, gin.H{"status": true, "token": instance.GenerateToken()})
}

func ChangeEmailView(c *gin.Context) {
	username := c.MustGet("user")
	if username == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not logged in."})
		return
	}

	var form ChangeEmailForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again.", "message": err.Error()})
		return
	}
	email := strings.TrimSpace(form.Email)
	if !utils.All(
		ValidateEmail(email),
		GeeTestCaptcha(form.Captcha),
	) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Email is not valid. Please check again."})
		return
	}

	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
	instance := &User{Username: username.(string)}
	if !instance.IsActive(db) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not activated."})
		return
	}

	if IsEmailExists(db, email) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Email already exists. Please try another email."})
		return
	}

	var oldEmail string
	err := db.QueryRow("SELECT email FROM auth WHERE username = ?", instance.Username).Scan(&oldEmail)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Server error. Please try again later.", "message": err.Error()})
		return
	}

	if oldEmail == email {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "New email cannot be the same as old email."})
		return
	}

	if rate := cache.Get(c, fmt.Sprintf(":mailrate:%s", email)); rate.Val() != "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "You can only change email once per 1 minutes."})
		return
	}

	if rate := cache.Get(c, fmt.Sprintf(":mailrate:%s", oldEmail)); rate.Val() != "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "You can only change email once per 1 minutes."})
		return
	}

	newCode := utils.GenerateCode(6)
	oldCode := utils.GenerateCode(6)
	cache.Set(c, fmt.Sprintf(":changeemail!mail:%s", instance.Username), email, 30*time.Minute)
	cache.Set(c, fmt.Sprintf(":changeemail!new:%s:%s", instance.Username, email), newCode, 30*time.Minute)
	cache.Set(c, fmt.Sprintf(":changeemail!old:%s:%s", instance.Username, oldEmail), oldCode, 30*time.Minute)

	cache.Set(c, fmt.Sprintf(":mailrate:%s", email), "1", 1*time.Minute)
	cache.Set(c, fmt.Sprintf(":mailrate:%s", oldEmail), "1", 1*time.Minute)
	go SendVerifyMail(email, newCode)
	go SendVerifyMail(oldEmail, oldCode)

	c.JSON(http.StatusOK, gin.H{"status": true})
}

func ChangeEmailVerifyView(c *gin.Context) {
	var form ChangeEmailVerifyForm
	if err := c.ShouldBind(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Form is not valid. Please check again.", "message": err.Error()})
		return
	}

	db, cache := utils.GetDBFromContext(c), utils.GetCacheFromContext(c)
	username := c.MustGet("user")
	if username == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not logged in."})
		return
	}

	instance := &User{Username: username.(string)}
	if !instance.IsActive(db) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "User is not activated."})
		return
	}

	var oldEmail string
	err := db.QueryRow("SELECT email FROM auth WHERE username = ?", instance.Username).Scan(&oldEmail)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Server error. Please try again later.", "message": err.Error()})
		return
	}

	newEmail := cache.Get(c, fmt.Sprintf(":changeemail!mail:%s", instance.Username)).Val()

	newCode := cache.Get(c, fmt.Sprintf(":changeemail!new:%s:%s", instance.Username, newEmail))
	oldCode := cache.Get(c, fmt.Sprintf(":changeemail!old:%s:%s", instance.Username, oldEmail))

	if form.New != newCode.Val() || form.Old != oldCode.Val() {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Your verification code is incorrect. Please check again."})
		return
	}

	if IsEmailExists(db, newEmail) {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Email already exists. Please try another email."})
		return
	}

	_, err = db.Query("UPDATE auth SET email = ? WHERE username = ?", newEmail, instance.Username)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "reason": "Server error. Please try again later.", "message": err.Error()})
		return
	}

	cache.Del(c, fmt.Sprintf(":changeemail!mail:%s", instance.Username))
	cache.Del(c, fmt.Sprintf(":changeemail!new:%s:%s", instance.Username, newEmail))
	cache.Del(c, fmt.Sprintf(":changeemail!old:%s:%s", instance.Username, oldEmail))

	c.JSON(http.StatusOK, gin.H{"status": true})
}
