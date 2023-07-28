package oauth

import (
	"deeptrain/utils"
	"fmt"
	"github.com/spf13/viper"
)

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
