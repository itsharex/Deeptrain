package auth

import (
	"deeptrain/utils"
	"fmt"
	"github.com/spf13/viper"
)

var headers = map[string]string{
	"Content-Type": "application/json",
}

type GeeTestRequest struct {
	CaptchaId     string `json:"captcha_id"`
	CaptchaOutput string `json:"captcha_output"`
	GenTime       string `json:"gen_time"`
	LotNumber     string `json:"lot_number"`
	PassToken     string `json:"pass_token"`
}

type RecaptchaResponse struct {
	RiskAnalysis struct {
		Score float64 `json:"score"`
	} `json:"riskAnalysis"`

	TokenProperties struct {
		Valid bool `json:"valid"`
	} `json:"tokenProperties"`
}

func InvisibleCaptcha(token string) (score float64) {
	if token == "" {
		return 0.
	}

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

	var resp RecaptchaResponse
	if resp, ok := data.(RecaptchaResponse); !(ok && resp.TokenProperties.Valid) {
		return 0.
	}
	return resp.RiskAnalysis.Score
}

func CheckCaptcha(token string) (score float64) {
	if token == "" {
		return 0.
	}

	uri := fmt.Sprintf(
		"https://recaptchaenterprise.googleapis.com/v1/projects/%s/assessments?key=%s",
		viper.GetString("recaptcha.project"),
		viper.GetString("recaptcha.apikey"),
	)

	data, err := utils.Post(uri, headers, map[string]interface{}{
		"event": map[string]interface{}{
			"token":   token,
			"siteKey": viper.GetString("recaptcha.register.sitekey"),
		},
	})
	if err != nil {
		return 0.
	}

	// data.(RecaptchaResponse) is not working here. I don't know how to solve it. So I use type converting here.
	if valid := data.(map[string]interface{})["tokenProperties"].(map[string]interface{})["valid"]; !valid.(bool) {
		return 0.
	}
	return data.(map[string]interface{})["riskAnalysis"].(map[string]interface{})["score"].(float64)
}

func GeeTestCaptcha(form GeeTestRequest) bool {
	id := viper.GetString("geetest.id")

	uri := fmt.Sprintf("https://gcaptcha4.geetest.com/validate??captcha_id=%s", id)
	data, err := utils.PostForm(uri, map[string]interface{}{
		"lot_number":     form.LotNumber,
		"pass_token":     form.PassToken,
		"captcha_id":     id,
		"captcha_output": form.CaptchaOutput,
		"gen_time":       form.GenTime,
		"sign_token":     utils.HmacEncrypt(viper.GetString("geetest.token"), form.LotNumber),
	})
	if err != nil {
		fmt.Println(err)
		return false
	}

	if data["status"] == "success" && data["result"] == "success" {
		return true
	}
	return false
}
