package auth

import (
	"deeptrain/utils"
	"fmt"
	"github.com/spf13/viper"
)

var headers = map[string]string{
	"Content-Type": "application/json",
}

type CaptchaResponse struct {
	RiskAnalysis struct {
		Score float64 `json:"score"`
	} `json:"riskAnalysis"`

	TokenProperties struct {
		Valid bool `json:"valid"`
	} `json:"tokenProperties"`
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

	var resp CaptchaResponse
	if resp, ok := data.(CaptchaResponse); !(ok && resp.TokenProperties.Valid) {
		return 0.
	}
	return resp.RiskAnalysis.Score
}
