package oauth

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
	"strings"
	"time"
)

type GithubRegisterForm struct {
	Code  string `json:"code" binding:"required"`
	Email string `json:"email" binding:"required"`
}

type GithubUser struct {
	Id        int    `json:"id"`
	Login     string `json:"login"`
	AvatarUrl string `json:"avatar_url"`
	Email     string `json:"email"`
}

func Validate(code string) string {
	uri := fmt.Sprintf("%s/login/oauth/access_token", viper.GetString("oauth.github.endpoint"))
	data, err := utils.PostForm(utils.PostFormRequest{
		Uri:    uri,
		Header: map[string]string{"Accept": "application/json"},
		Body: map[string]interface{}{
			"client_id":     viper.GetString("oauth.github.client_id"),
			"client_secret": viper.GetString("oauth.github.client_secret"),
			"code":          code,
		}})
	if err != nil {
		return ""
	}

	token, ok := data["access_token"].(string)
	if !ok {
		return ""
	}
	return token
}

func GetInfo(token string) *GithubUser {
	uri := fmt.Sprintf("%s/user", viper.GetString("oauth.github.api_endpoint"))
	data, err := utils.Get(uri, map[string]string{"Authorization": fmt.Sprintf("token %s", token)})
	if err != nil {
		return nil
	}
	var user GithubUser
	if err := utils.MapToStruct(data, &user); err != nil {
		return nil
	}
	return &user
}

func GithubRegisterView(c *gin.Context) {
	var form GithubRegisterForm
	if err := c.ShouldBindJSON(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": err.Error()})
		return
	}

	if !auth.ValidateEmail(form.Email) || form.Code == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid email or code"})
		return
	}

	cache := utils.GetCacheFromContext(c)
	data, err := cache.Get(c, fmt.Sprintf("oauth:github:%s", form.Code)).Result()
	if err != nil || data == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	var user GithubUser
	if err := json.Unmarshal([]byte(data), &user); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	db := utils.GetDBFromContext(c)
	if auth.IsEmailExists(db, form.Email) {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "The email is already registered"})
		return
	}

	if auth.IsUserExists(db, user.Login) {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "The username is already registered"})
		return
	}

	raw := utils.GenerateChar(16)
	hash := utils.Sha2Encrypt(raw)

	instance := &auth.User{
		Username: user.Login,
		Password: hash,
		Email:    form.Email,
		Active:   false,
	}

	instance.Save(db)
	id := instance.GetID(db)

	_, err = db.Exec("INSERT INTO oauth (user_id, provider, provider_id) VALUES (?, ?, ?)", id, "github", user.Id)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "internal error"})
		return
	}

	cache.Del(c, fmt.Sprintf("oauth:github:%s", form.Code))

	code := utils.GenerateCode(6)
	cache.Set(c, fmt.Sprintf(":verify:%s", user.Login), code, 30*time.Minute)
	cache.Set(c, fmt.Sprintf(":mailrate:%s", form.Email), "1", 1*time.Minute)
	go auth.SendVerifyMail(form.Email, code)
	go auth.SaveAvatar(user.Login)

	c.JSON(http.StatusOK, gin.H{"status": true, "token": instance.GenerateToken()})
}

func GithubPreFlightView(c *gin.Context) {
	code := strings.TrimSpace(c.Query("code"))
	if code == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "code is required"})
		return
	}

	token := Validate(code)
	if token == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	user := GetInfo(token)
	if user == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	db := utils.GetDBFromContext(c)
	if IsOAuthExist(db, "github", user.Id) {
		// login
		instance := GetUserFromOAuth(db, "github", user.Id)
		c.JSON(http.StatusOK, gin.H{"status": true, "token": instance.GenerateToken(), "username": instance.Username, "register": false})
	}

	cache := utils.GetCacheFromContext(c)
	data, err := json.Marshal(user)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "internal error"})
		return
	}
	if err := cache.Set(c, fmt.Sprintf("oauth:github:%s", code), data, time.Minute*5).Err(); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "internal error"})
		return
	}

	if auth.IsUserExists(db, user.Login) {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "The username is already registered"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status":   true,
		"email":    user.Email,
		"username": user.Login,
		"register": true,
	})
}
