package oauth

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
	"time"
)

func AsStruct[T comparable](data interface{}) *T {
	var result T
	if err := utils.MapToStruct(data, &result); err != nil {
		return nil
	}
	return &result
}

func GetId(id string) int {
	if v, err := strconv.Atoi(id); err == nil {
		return utils.Abs(v)
	}

	return utils.Abs(utils.Sha2EncryptToInt(id))
}

func GetPreflightCodeFromCache(c *gin.Context, provider string, code string) string {
	cache := utils.GetCacheFromContext(c)
	data, err := cache.Get(c, fmt.Sprintf("oauth:%s:%s", provider, code)).Result()
	if err != nil {
		return ""
	}
	return data
}

func GetPreflightCode[T comparable](c *gin.Context, provider string, code string) *T {
	data := GetPreflightCodeFromCache(c, provider, code)
	if data == "" {
		return nil
	}

	var result T
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		return nil
	}

	return &result
}

func CreateUser(c *gin.Context, provider string, username string, email string, token string, providerId int) (*auth.User, error) {
	db := utils.GetDBFromContext(c)

	if auth.IsEmailExists(db, email) {
		return nil, errors.New("the email is already registered")
	}

	if auth.IsUserExists(db, username) {
		return nil, errors.New("the username is already registered")
	}

	instance := &auth.User{
		Username: username,
		Password: utils.GenerateCharWithSha256(16),
		Email:    email,
		Active:   false,
	}

	instance.Save(db)
	id := instance.GetID(db)

	if err := AddOAuthConnection(db, id, provider, providerId); err != nil {
		return nil, errors.New("internal error")
	}

	cache := utils.GetCacheFromContext(c)

	cache.Del(c, fmt.Sprintf("oauth:%s:%s", provider, token))

	code := utils.GenerateCode(6)
	cache.Set(c, fmt.Sprintf(":verify:%s", username), code, 30*time.Minute)
	cache.Set(c, fmt.Sprintf(":mailrate:%s", email), "1", 1*time.Minute)
	go auth.SendVerifyMail(email, code)
	go auth.SaveAvatar(username)

	return instance, nil
}

func PreflightUser(c *gin.Context, instance interface{}, provider string, username string, email string, token string, providerId int) {
	db := utils.GetDBFromContext(c)
	if IsOAuthExist(db, provider, providerId) {
		// login
		instance := GetUserFromOAuth(db, provider, providerId)
		c.JSON(http.StatusOK, gin.H{"status": true, "token": instance.GenerateToken(), "username": instance.Username, "register": false})
		return
	}

	// register
	cache := utils.GetCacheFromContext(c)
	data, err := json.Marshal(instance)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "internal error"})
		return
	}
	if err := cache.Set(c, fmt.Sprintf("oauth:%s:%s", provider, token), data, time.Minute*5).Err(); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "internal error"})
		return
	}

	if auth.IsUserExists(db, username) {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "The username is already registered"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status":   true,
		"email":    email,
		"username": username,
		"register": true,
	})
}

func ConnectUser(c *gin.Context, provider string, username string, providerId int) error {
	db := utils.GetDBFromContext(c)
	user := &auth.User{Username: username}

	if IsUserConnected(db, user.GetID(db), provider) {
		return errors.New("the account has been connected to " + provider)
	}

	if IsOAuthExist(db, provider, providerId) {
		return errors.New("the account has been connected to " + provider)
	}

	if err := AddOAuthConnection(db, user.GetID(db), provider, providerId); err != nil {
		return errors.New("internal error")
	}

	return nil
}
