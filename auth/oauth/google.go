package oauth

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
	"strings"
)

type GoogleRegisterForm struct {
	Code  string `json:"code" binding:"required"`
	Email string `json:"email" binding:"required"`
}

type GoogleUser struct {
	Id       string `json:"id"`
	Email    string `json:"email"`
	Verified bool   `json:"verified_email"`
	Picture  string `json:"picture"`
}

func ValidateGoogleAPI(code string) string {
	uri := fmt.Sprintf("%s/token", viper.GetString("oauth.google.endpoint"))
	data, err := utils.PostForm(utils.PostFormRequest{
		Uri:    uri,
		Header: map[string]string{"Content-Type": "application/json", "Accept": "application/json"},
		Body: map[string]interface{}{
			"client_id":     viper.GetString("oauth.google.client_id"),
			"client_secret": viper.GetString("oauth.google.client_secret"),
			"code":          code,
			"grant_type":    "authorization_code",
			"redirect_uri":  viper.GetString("oauth.google.redirect_uri"),
		},
	})

	if err != nil {
		return ""
	}

	token, ok := data["access_token"].(string)
	if !ok {
		return ""
	}
	return token
}

func GetUsername(email string) string {
	if strings.HasSuffix(email, "@gmail.com") {
		return strings.Split(email, "@")[0]
	}
	return email
}

func GetGoogleInfo(token string) *GoogleUser {
	uri := fmt.Sprintf("%s/oauth2/v2/userinfo", viper.GetString("oauth.google.api_endpoint"))
	data, err := utils.Get(uri, map[string]string{
		"Content-Type":  "application/json",
		"Accept":        "application/json",
		"Authorization": fmt.Sprintf("Bearer %s", token),
	})

	if err != nil {
		return nil
	}

	return AsStruct[GoogleUser](data)
}

func GoogleRegisterView(c *gin.Context) {
	var form GoogleRegisterForm
	if err := c.ShouldBindJSON(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": err.Error()})
		return
	}

	if !auth.ValidateEmail(form.Email) || form.Code == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid email or code"})
		return
	}

	user := GetPreflightCode[GoogleUser](c, "google", form.Code)
	if user == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	instance, err := CreateUser(c, "google", GetUsername(form.Email), form.Email, form.Code, GetId(user.Id))
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": true, "token": instance.GenerateToken()})
}

func GooglePreFlightView(c *gin.Context) {
	code := GetCode(c)
	if code == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "code is required"})
		return
	}

	token := ValidateGoogleAPI(code)
	if token == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	user := GetGoogleInfo(token)
	if user == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	PreflightUser(c, user, "google", GetUsername(user.Email), user.Email, code, GetId(user.Id))
}

func GoogleConnectView(c *gin.Context) {
	username := c.MustGet("user").(string)
	code := GetCode(c)

	if username == "" || code == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	token := ValidateGoogleAPI(code)
	if token == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	i := GetGoogleInfo(token)
	if i == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	err := ConnectUser(c, "google", username, GetId(i.Id))
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": true})
}
