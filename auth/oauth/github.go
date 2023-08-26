package oauth

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
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

func ValidateGithubAPI(code string) string {
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

func GetGithubInfo(token string) *GithubUser {
	uri := fmt.Sprintf("%s/user", viper.GetString("oauth.github.api_endpoint"))
	data, err := utils.Get(uri, map[string]string{"Authorization": fmt.Sprintf("token %s", token)})
	if err != nil {
		return nil
	}

	return AsStruct[GithubUser](data)
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

	user := GetPreflightCode[GithubUser](c, "github", form.Code)
	if user == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	instance, err := CreateUser(c, "github", user.Login, form.Email, form.Code, user.Id)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": true, "token": instance.GenerateToken()})
}

func GithubPreFlightView(c *gin.Context) {
	code := GetCode(c)
	if code == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "code is required"})
		return
	}

	token := ValidateGithubAPI(code)
	if token == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	user := GetGithubInfo(token)
	if user == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	PreflightUser(c, user, "github", user.Login, user.Email, code, user.Id)
}

func GithubConnectView(c *gin.Context) {
	username := c.MustGet("user").(string)
	code := GetCode(c)

	if username == "" || code == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	token := ValidateGithubAPI(code)
	if token == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid code"})
		return
	}

	i := GetGithubInfo(token)
	if i == nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	err := ConnectUser(c, "github", username, i.Id)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": true})
}
