package pay

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
	"strings"
)

type RequestCertForm struct {
	Name    string              `json:"name" binding:"required"`
	Id      string              `json:"id" binding:"required"`
	Captcha auth.GeeTestRequest `json:"captcha" binding:"required"`
}

type RequestPayForm struct {
	Amount float32 `json:"amount" binding:"required"`
	Mobile bool    `json:"mobile"`
	Type   string  `json:"type" binding:"required"`
}

func RequireAuthByCtx(c *gin.Context) *auth.User {
	user := c.MustGet("user").(string)
	if user == "" {
		c.JSON(http.StatusOK, gin.H{
			"status": true,
			"error":  "authentication failed",
		})
		return nil
	}
	return &auth.User{Username: user}
}

func RefreshCertView(c *gin.Context) {
	user := RequireAuthByCtx(c)
	if user == nil {
		return
	}

	db := utils.GetDBFromContext(c)
	if !RefreshCert(db, user) {
		c.JSON(http.StatusOK, gin.H{
			"status": true,
			"error":  "refresh failed",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": true,
		"error":  "",
	})
}

func RequestCertView(c *gin.Context) {
	var form RequestCertForm
	if err := c.ShouldBindJSON(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	user := RequireAuthByCtx(c)
	if user == nil {
		return
	}

	name, no := strings.TrimSpace(form.Name), strings.TrimSpace(form.Id)
	if !utils.All(ValidateName(name), ValidateNo(no)) {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  "invalid name or number",
		})
		return
	}

	if !auth.GeeTestCaptcha(form.Captcha) {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  "invalid captcha",
		})
		return
	}

	db := utils.GetDBFromContext(c)
	uri, err := NewCertRequest(db, user, name, no)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": true,
		"error":  "",
		"uri":    uri,
	})
}

func GetCertStateView(c *gin.Context) {
	user := RequireAuthByCtx(c)
	if user == nil {
		return
	}

	db := utils.GetDBFromContext(c)
	if !HasRecord(db, user) {
		c.JSON(http.StatusOK, gin.H{
			"state": 0,
		})
		return
	}

	name, no, id, err := GetCert(db, user)
	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"state": 0,
			"error": err.Error(),
		})
		return
	}

	var state int
	var link string
	if HasValidCert(db, user) {
		state = 2
	} else {
		if RefreshCert(db, user) && HasValidCert(db, user) {
			state = 2
		} else {
			state = 1
			link, _ = CreateCertRequest(id)
			link = utils.GetQRCode(id, link)
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"state": state,
		"name":  name,
		"no":    no,
		"link":  link,
	})
}

func GetCertQRCodeView(c *gin.Context) {
	utils.GetQRCodeResponse(c, c.Query("id"))
}

func CreatePaymentView(c *gin.Context) {
	var form RequestPayForm
	if err := c.ShouldBindJSON(&form); err != nil {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	user := RequireAuthByCtx(c)
	if user == nil {
		return
	}

	if form.Amount < 0.01 || form.Amount > 20000 {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  "invalid amount",
		})
		return
	}

	db := utils.GetDBFromContext(c)

	var url string
	var err error

	if form.Type == "alipay" {
		url, err = NewAlipayOrder(db, user, form.Amount, form.Mobile)
	} else if form.Type == "wechat" {
		url, err = NewWechatOrder(db, user, form.Amount， form.Mobile)
	} else {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  "invalid payment type",
		})
		return
	}

	if err != nil {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": true,
		"url":    url,
	})
	return
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
