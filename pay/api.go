package pay

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

type RequestCertForm struct {
	Name    string              `json:"name" binding:"required"`
	Id      string              `json:"id" binding:"required"`
	Captcha auth.GeeTestRequest `json:"captcha" binding:"required"`
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
