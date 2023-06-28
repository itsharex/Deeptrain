package auth

import (
	"bytes"
	"deeptrain/utils"
	"text/template"
)

func SendVerifyMail(to string, code string) error {
	subject := "Deeptrain - Verify your email"

	tmpl, err := template.New("verify.html").ParseFiles("auth/templates/verify.html")
	if err != nil {
		return err
	}

	var buf bytes.Buffer
	err = tmpl.ExecuteTemplate(&buf, "verify.html", struct {
		Code string
	}{code})
	if err != nil {
		return err
	}

	utils.SendMail(to, subject, buf.String())
	return nil
}
