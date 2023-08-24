package pay

import (
	"context"
	"deeptrain/utils"
	"fmt"
	"github.com/go-pay/gopay"
	"github.com/spf13/viper"
	"regexp"
	"strconv"
	"time"
)

func ValidateName(name string) bool {
	return len([]rune(name)) >= 2
}

func ValidateId(id string) bool {
	pattern := `^(\d{17}[\dXx])|(\d{15})$`
	matched, _ := regexp.MatchString(pattern, id)
	if !matched {
		return false
	}

	code := []string{"1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"}

	weights := []int{7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2}
	checker := 0
	for i, char := range id[:17] {
		digit, err := strconv.Atoi(string(char))
		if err != nil {
			return false
		}
		checker += digit * weights[i]
	}

	remainder := checker % 11
	if id[17:] != code[remainder] {
		return false
	}

	return true
}

func InitCertRequest(id, name, no string) string {
	instance := make(gopay.BodyMap)
	instance.Set("outer_order_no", id)
	instance.Set("biz_code", "FACE")
	instance.Set("identity_param", map[string]string{
		"identity_type": "CERT_INFO",
		"cert_type":     "IDENTITY_CARD",
		"cert_name":     name,
		"cert_no":       no,
	})
	instance.Set("merchant_config", map[string]string{
		"return_url": viper.GetString("pay.cert.return_url"),
	})

	ctx := context.Background()
	resp, err := aliClient.UserCertifyOpenInit(ctx, instance)
	if err != nil {
		fmt.Println(err.Error())
		return ""
	}

	return resp.Response.CertifyId
}

func CreateCertRequest(id string) string {
	instance := make(gopay.BodyMap)
	instance.Set("certify_id", id)

	ctx := context.Background()
	url, err := aliClient.UserCertifyOpenCertify(ctx, instance)
	if err != nil {
		fmt.Println(err.Error())
		return ""
	}

	return url
}

func VerifyCertRequest(id string) bool {
	instance := make(gopay.BodyMap)
	instance.Set("certify_id", id)

	ctx := context.Background()
	resp, err := aliClient.UserCertifyOpenQuery(ctx, instance)
	if err != nil {
		fmt.Println(err.Error())
		return false
	}

	return resp.Response.Passed == "T"
}

func GenerateCertHash(name, no string) string {
	// return 32-bit order id
	t := time.Now().Format("20060102150405")
	r := utils.GenerateCode(6)
	return utils.Md5Encrypt(name + no + t)[:26] + r
}
