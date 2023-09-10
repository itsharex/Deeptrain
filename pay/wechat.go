package pay

import (
	"context"
	"database/sql"
	"deeptrain/auth"
	"deeptrain/utils"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"github.com/wechatpay-apiv3/wechatpay-go/core"
	"github.com/wechatpay-apiv3/wechatpay-go/core/auth/verifiers"
	"github.com/wechatpay-apiv3/wechatpay-go/core/downloader"
	"github.com/wechatpay-apiv3/wechatpay-go/core/notify"
	"github.com/wechatpay-apiv3/wechatpay-go/core/option"
	"github.com/wechatpay-apiv3/wechatpay-go/services/payments"
	"github.com/wechatpay-apiv3/wechatpay-go/services/payments/native"
	weutil "github.com/wechatpay-apiv3/wechatpay-go/utils"
	"time"
)

var wechatClient *core.Client
var wechatService *native.NativeApiService
var wechatHandler *notify.Handler

func InitWechatClient() {
	ctx := context.Background()

	privateKey := utils.TryWithPanic(weutil.LoadPrivateKeyWithPath(viper.GetString("pay.wechat.cert_path")))

	opts := []core.ClientOption{
		option.WithWechatPayAutoAuthCipher(
			viper.GetString("pay.wechat.merchant_id"),
			viper.GetString("pay.wechat.serial_no"),
			privateKey,
			viper.GetString("pay.wechat.key"),
		),
	}
	wechatClient = utils.TryWithPanic(core.NewClient(ctx, opts...))
	wechatService = &native.NativeApiService{
		Client: wechatClient,
	}

	utils.TryPanic(downloader.MgrInstance().RegisterDownloaderWithPrivateKey(
		ctx, privateKey,
		viper.GetString("pay.wechat.serial_no"),
		viper.GetString("pay.wechat.merchant_id"),
		viper.GetString("pay.wechat.key"),
	))
	wechatHandler = utils.TryWithPanic(notify.NewRSANotifyHandler(
		viper.GetString("pay.wechat.key"),
		verifiers.NewSHA256WithRSAVerifier(downloader.MgrInstance().GetCertificateVisitor(viper.GetString("pay.wechat.merchant_id"))),
	))
}

func CreateWechatPay(subject string, id string, amount float32) (url string) {
	ctx := context.Background()
	resp, result, err := wechatService.Prepay(ctx, native.PrepayRequest{
		Appid:       core.String(viper.GetString("pay.wechat.app_id")),
		Mchid:       core.String(viper.GetString("pay.wechat.merchant_id")),
		Description: core.String(subject),
		OutTradeNo:  core.String(id),
		NotifyUrl:   core.String(viper.GetString("pay.wechat.notify_url")),
		Amount: &native.Amount{
			Total: core.Int64(int64(amount * 100)),
		},
		TimeExpire: core.Time(time.Now().Add(30 * time.Minute)),
	})

	if result == nil || err != nil {
		fmt.Println(err.Error())
		return ""
	}

	return *resp.CodeUrl
}

func NewWechatOrder(db *sql.DB, user *auth.User, amount float32, isMobile bool) (string, error) {
	id, err := NewOrderExec("wechat", db, user, amount)
	if err != nil {
		return "", err
	}

	uri := CreateWechatPay("DeepTrain", id, amount)
	if uri == "" {
		return "", fmt.Errorf("create wechat pay order failed")
	}

	link := utils.GetQRCode(id, uri)
	return link, nil
}

func VerifyWechatReturn(ctx *gin.Context) {
	transaction := new(payments.Transaction)
	notifyReq, err := wechatHandler.ParseNotifyRequest(context.Background(), ctx.Request, transaction)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(notifyReq.Summary)
	fmt.Println(transaction.TransactionId)

}
