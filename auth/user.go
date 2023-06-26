package auth

import "deeptrain/connection"

type User struct {
	Username string
	Password string
	Email    string
	Active   bool
	CreateAt string
	IsAdmin  bool
}

func isUserExists(username string) (bool, error) {
	var count int
	err := connection.DB.QueryRow("SELECT COUNT(*) FROM auth WHERE username = ?", username).Scan(&count)
	if err != nil {
		return false, err
	}
	return count > 0, nil
}

func (u *User) GenerateToken() string {
	return ""
}
