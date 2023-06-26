package auth

import (
	"deeptrain/utils"
	"regexp"
	"strings"
)

var mailSuffixes = []string{
	"gmail.com",
	"outlook.com",
	"163.com",
	"qq.com",
	"deeptrain.net",
}

func ValidateUsername(username string) bool {
	length := len(username)
	return length >= 3 && length <= 14
}

func ValidatePassword(password string) bool {
	length := len(password)
	return length >= 6 && length <= 26
}

func ValidateEmail(value string) bool {
	res := strings.Split(strings.TrimSpace(value), "@")
	if len(res) != 2 || res[0] == "" || res[1] == "" {
		return false
	}
	mail, suffix := res[0], res[1]
	if !regexp.MustCompile(`^\S+$`).MatchString(mail) {
		return false
	}
	return utils.Contains(mailSuffixes, suffix)
}
