package auth

import (
	"deeptrain/utils"
	"fmt"
	"github.com/spf13/viper"
)

var headers = map[string]string{
	"Content-Type": "application/json",
}

var loginUri = fmt.Sprintf(
	"https://recaptchaenterprise.googleapis.com/v1/projects/%s/assessments?key=%s",
	viper.Get("recaptcha.project_id"),
	viper.Get("recaptcha.api_key"),
)

func login(token string) (score float64) {
	data, err := utils.Post(loginUri, headers, map[string]interface{}{
		"event": map[string]interface{}{
			"token":          token,
			"siteKey":        viper.Get("recaptcha.site_key"),
			"expectedAction": "login",
		},
	})
	if err != nil {
		return 0.
	}
	return data.(map[string]interface{})["riskAnalysis"].(map[string]interface{})["score"].(float64)
}
