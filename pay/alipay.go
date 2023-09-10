package pay

import (
	"context"
	"database/sql"
	"deeptrain/auth"
	"deeptrain/utils"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/go-pay/gopay"
	"github.com/go-pay/gopay/alipay"
	"github.com/spf13/viper"
)

var aliClient *alipay.Client
var pageSize = 5

type Notify struct {
	Body        string `json:"body"`
	BuyerId     string `json:"buyer_id"`
	TotalAmount string `json:"total_amount"`
	TradeNo     string `json:"trade_no"`
	OutTradeNo  string `json:"out_trade_no"`
	TradeStatus string `json:"trade_status"`
}

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

func VerifyAliPayNotify(c *gin.Context) (*Notify, error) {
	notify, err := alipay.ParseNotifyToBodyMap(c.Request)
	if err != nil {
		return nil, err
	}

	if ok, err := alipay.VerifySign(viper.GetString("pay.alipay.public_key"), notify); err != nil || !ok {
		return nil, err
	}

	var result Notify
	if err := notify.Unmarshal(&result); err != nil {
		return nil, err
	}

	return &result, nil
}

func VerifyAliPayReturn(c *gin.Context) {
	// on success, return 200 with response "success" to alipay
	// on failure, return 400

	res, err := VerifyAliPayNotify(c)
	if err != nil {
		c.String(400, err.Error())
		return
	}

	if res.TradeStatus == "TRADE_SUCCESS" {
		db := utils.GetDBFromContext(c)
		err = FinishPayment(db, res.OutTradeNo, res.TotalAmount)
		if err != nil {
			c.String(400, err.Error())
			return
		}
	}

	c.JSON(200, "success")
}

func NewAlipayOrder(db *sql.DB, user *auth.User, amount float32, mobile bool) (string, error) {
	id, err := NewOrderExec("alipay", db, user, amount)
	if err != nil {
		return "", err
	}

	uri := CreateAliPay("DeepTrain", id, amount, mobile)
	if uri == "" {
		return "", fmt.Errorf("create alipay order failed")
	}

	return uri, nil
}
