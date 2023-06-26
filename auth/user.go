package auth

import (
	"database/sql"
	"deeptrain/utils"
	"github.com/dgrijalva/jwt-go"
	"github.com/spf13/viper"
	"time"
)

type User struct {
	Username string
	Password string
	Email    string
	Active   bool
	CreateAt string
	IsAdmin  bool
}

func isUserExists(db *sql.DB, username string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM auth WHERE username = ?", username).Scan(&count)
	if err != nil {
		return true
	}
	return count > 0
}

func isEmailExists(db *sql.DB, email string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM auth WHERE email = ?", email).Scan(&count)
	if err != nil {
		return true
	}
	return count > 0
}

func ValidateUser(db *sql.DB, username string, raw string) bool {
	var count int
	password := utils.Sha2Encrypt(raw)
	err := db.QueryRow("SELECT COUNT(*) FROM auth WHERE username = ? AND password = ?", username, password).Scan(&count)
	if err != nil {
		return false
	}
	return count > 0
}

func ParseToken(token string) *User {
	instance, err := jwt.Parse(token, func(token *jwt.Token) (interface{}, error) {
		return []byte(viper.GetString("secret")), nil
	})
	if err != nil {
		return nil
	}
	if claims, ok := instance.Claims.(jwt.MapClaims); ok && instance.Valid {
		if claims["exp"].(float64) < float64(time.Now().Unix()) {
			return nil
		}
		return &User{
			Username: claims["username"].(string),
			Password: claims["password"].(string),
		}
	}
	return nil
}

func (u *User) GenerateToken() string {
	instance := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"username": u.Username,
		"password": u.Password,
		"exp":      time.Now().Add(time.Hour * 24 * 30).Unix(),
	})
	token, err := instance.SignedString([]byte(viper.GetString("secret")))
	if err != nil {
		return ""
	}
	return token
}

func (u *User) Save(db *sql.DB) bool {
	_, err := db.Exec(
		"INSERT INTO auth (username, password, email, active, is_admin) VALUES (?, ?, ?, ?, ?)",
		u.Username, u.Password, u.Email, u.Active, u.IsAdmin,
	)
	if err != nil {
		return false
	}
	return true
}
