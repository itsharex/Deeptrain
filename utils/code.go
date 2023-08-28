package utils

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/skip2/go-qrcode"
)

func GenerateQRCode(link string, path string) error {
	qr, err := qrcode.New(link, qrcode.Low)
	if err != nil {
		return err
	}
	return qr.WriteFile(256, path)
}

func GetQRCodePath(salt string) string {
	return fmt.Sprintf("storage/qrcode/%s.png", Md5Encrypt(salt))
}

func GetQRCode(salt, link string) string {
	hash := Md5Encrypt(salt)
	path := fmt.Sprintf("storage/qrcode/%s.png", hash)
	if !FileExists(path) {
		GenerateQRCode(link, path)
	}
	return hash
}

func GetQRCodeResponse(c *gin.Context, hash string) {
	path := fmt.Sprintf("storage/qrcode/%s.png", hash)
	if !FileExists(path) {
		c.JSON(200, gin.H{
			"status": false,
			"error":  "QR code not found",
		})
		return
	}

	c.File(path)
}
