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
	"github.com/go-pay/gopay/pkg/util"
	"github.com/spf13/viper"
	"strconv"
	"time"
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

func FinishPayment(db *sql.DB, id string, amount string) error {
	_, err := db.Exec(`
		UPDATE payment_log
		SET payment_status = TRUE
		WHERE order_id = ? AND amount = ? AND payment_status = FALSE
	`, id, amount)
	if err != nil {
		return err
	}

	user := auth.User{}
	err = db.QueryRow(`SELECT user_id FROM payment_log WHERE order_id = ?`, id).Scan(&user.ID)
	if err != nil {
		return err
	}

	// create payment if not exists
	_, err = db.Exec(`
		INSERT INTO payment (user_id, amount, total_amount)
		VALUES (?, ?, ?)
		ON DUPLICATE KEY UPDATE amount = amount + ?, total_amount = total_amount + ?
	`, user.ID, amount, amount, amount, amount)
	if err != nil {
		return err
	}

	return nil
}

func GetTradeStatusView(c *gin.Context) {
	db := utils.GetDBFromContext(c)
	var id string
	err := db.QueryRow(`SELECT order_id FROM payment_log WHERE order_id = ? AND payment_status = TRUE`, c.Query("id")).Scan(&id)
	if err != nil {
		c.JSON(200, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	c.JSON(200, gin.H{
		"status": true,
		"error":  "",
	})
}

func GetAmountView(c *gin.Context) {
	user := RequireAuthByCtx(c)
	if user == nil {
		return
	}

	db := utils.GetDBFromContext(c)
	var amount float32
	err := db.QueryRow(`SELECT amount FROM payment WHERE user_id = ?`, user.GetID(db)).Scan(&amount)
	if err != nil {
		fmt.Println(err.Error())
		c.JSON(200, gin.H{
			"status": true,
			"amount": 0.,
		})
		return
	}

	c.JSON(200, gin.H{
		"status": true,
		"amount": amount,
	})
}

func GetPaymentLogView(c *gin.Context) {
	user := RequireAuthByCtx(c)
	if user == nil {
		return
	}

	page := utils.ParseInt(c.Query("page"), 1) - 1

	var total int
	db := utils.GetDBFromContext(c)
	err := db.QueryRow(`SELECT COUNT(*) FROM payment_log WHERE user_id = ?`, user.GetID(db)).Scan(&total)
	if err != nil {
		c.JSON(200, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	totalPage := total / pageSize
	if total%pageSize != 0 {
		totalPage++
	}

	if page >= totalPage {
		page = totalPage - 1
	} else if page < 0 {
		page = 0
	}

	logs := make([]gin.H, 0)
	rows, err := db.Query(`
		SELECT order_id, amount, payment_type, payment_status, created_at
		FROM payment_log
		WHERE user_id = ?
		ORDER BY created_at DESC
		LIMIT ?, 
	`+strconv.Itoa(pageSize), user.GetID(db), page*pageSize)
	if err != nil {
		c.JSON(200, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}
	defer rows.Close()

	for rows.Next() {
		var (
			orderId       string
			amount        float32
			paymentType   string
			paymentStatus bool
			createdAt     []uint8
		)
		err := rows.Scan(&orderId, &amount, &paymentType, &paymentStatus, &createdAt)
		if err != nil {
			c.JSON(200, gin.H{
				"status": false,
				"error":  err.Error(),
			})
			return
		}

		logs = append(logs, gin.H{
			"order":  orderId,
			"amount": amount,
			"type":   paymentType,
			"state":  paymentStatus,
			"time":   utils.ConvertTime(createdAt).Format("2006-01-02 15:04:05"),
		})
	}

	c.JSON(200, gin.H{
		"status": true,
		"data":   logs,
		"total":  totalPage,
	})
}

func VerifyAliPayReturn(c *gin.Context) {
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

func NewOrderExec(db *sql.DB, user *auth.User, amount float32) (string, error) {
	// return 32-bit id
	date := time.Now().Format("20060102150405")
	id := fmt.Sprintf("%s%s", date, utils.Sha2Encrypt(fmt.Sprintf("alipay%s%s", date, user.Username))[:16]) + util.RandomNumber(2)

	_, err := db.Exec(`
		INSERT INTO payment_log (user_id, order_id, amount, payment_type)
		VALUES (?, ?, ?, ?)
	`, user.GetID(db), id, amount, "alipay")
	if err != nil {
		return "", err
	}

	return id, nil
}

func NewAlipayOrder(db *sql.DB, user *auth.User, amount float32, mobile bool) (string, error) {
	id, err := NewOrderExec(db, user, amount)
	if err != nil {
		return "", err
	}

	uri := CreateAliPay("DeepTrain", id, amount, mobile)
	if uri == "" {
		return "", fmt.Errorf("create alipay order failed")
	}

	return uri, nil
}
