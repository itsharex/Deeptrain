package pay

import (
	"context"
	"deeptrain/utils"
	"fmt"
	"github.com/go-pay/gopay"
	"github.com/go-pay/gopay/alipay"
	"github.com/spf13/viper"
)

var aliClient *alipay.Client

func InitAliClient() {
	aliClient = utils.TryWithPanic(alipay.NewClient(viper.GetString("pay.alipay.app_id"), viper.GetString("pay.alipay.private_key"), viper.GetBool("pay.alipay.is_prod")))
	aliClient.SetCharset("utf-8")
	aliClient.SetSignType(alipay.RSA2)
	aliClient.SetReturnUrl(viper.GetString("pay.alipay.return_url"))
	aliClient.SetNotifyUrl(viper.GetString("pay.alipay.notify_url"))
}

func CreateAliPay(subject string, id string, amount float32, isMobile bool) (url string) {
	instance := make(gopay.BodyMap)
	instance.Set("subject", subject)
	instance.Set("out_trade_no", id)
	instance.Set("total_amount", fmt.Sprintf("%.2f", amount))
	instance.Set("timeout_express", "30m")
	instance.Set("product_code", "FAST_INSTANT_TRADE_PAY")

	ctx := context.Background()

	var err error

	if isMobile {
		url, err = aliClient.TradeWapPay(ctx, instance)
	} else {
		url, err = aliClient.TradePagePay(ctx, instance)
	}
	if err != nil {
		fmt.Println(err.Error())
	}

	return url
}
