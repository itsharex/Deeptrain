package auth

import (
	"deeptrain/utils"
	"fmt"
	"github.com/spf13/viper"
)

var headers = map[string]string{
	"Content-Type": "application/json",
}

func LoginCaptcha(token string) (score float64) {
	uri := fmt.Sprintf(
		"https://recaptchaenterprise.googleapis.com/v1/projects/%s/assessments?key=%s",
		viper.GetString("recaptcha.project"),
		viper.GetString("recaptcha.apikey"),
	)

	data, err := utils.Post(uri, headers, map[string]interface{}{
		"event": map[string]interface{}{
			"token":          token,
			"siteKey":        viper.GetString("recaptcha.login.sitekey"),
			"expectedAction": "login",
		},
	})
	if err != nil {
		return 0.
	}
	return data.(map[string]interface{})["riskAnalysis"].(map[string]interface{})["score"].(float64)
}
