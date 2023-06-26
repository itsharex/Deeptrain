package auth

func CheckUsername(username string) bool {
	length := len(username)
	return length >= 3 && length <= 14
}

func CheckPassword(password string) bool {
	length := len(password)
	return length >= 6 && length <= 26
}

func CheckEmail(email string) bool {

}
