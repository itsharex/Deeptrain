package auth

import (
	"bytes"
	"deeptrain/utils"
	"text/template"
)

func SendVerifyMail(to string, code string) error {
	subject := "[Deeptrain] Verify your email"

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

func SendWelcomeMail(username string, to string) error {
	subject := "[Deeptrain] Welcome to Deeptrain"

	tmpl, err := template.New("registration.html").ParseFiles("auth/templates/registration.html")
	if err != nil {
		return err
	}

	var buf bytes.Buffer
	err = tmpl.ExecuteTemplate(&buf, "registration.html", struct {
		Name string
	}{username})
	if err != nil {
		return err
	}

	utils.SendMail(to, subject, buf.String())
	return nil
}

func SendResetMail(to string, code string) error {
	subject := "[Deeptrain] Reset your password"

	tmpl, err := template.New("reset.html").ParseFiles("auth/templates/reset.html")
	if err != nil {
		return err
	}

	var buf bytes.Buffer
	err = tmpl.ExecuteTemplate(&buf, "reset.html", struct {
		Code string
	}{code})
	if err != nil {
		return err
	}

	utils.SendMail(to, subject, buf.String())
	return nil
}
