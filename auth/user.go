package auth

import (
	"context"
	"database/sql"
	"deeptrain/connection"
	"fmt"
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

func ParseToken(ctx context.Context, db *sql.DB, token string) *User {
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
		user := &User{
			Username: claims["username"].(string),
			Password: claims["password"].(string),
		}
		if user.Validate(db, ctx) {
			return user
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

func (u *User) Delete(db *sql.DB) bool {
	_, err := db.Exec("DELETE FROM auth WHERE username = ?", u.Username)
	if err != nil {
		return false
	}
	return true
}

func (u *User) IsActive(db *sql.DB) bool {
	var active bool
	err := db.QueryRow("SELECT active FROM auth WHERE username = ?", u.Username).Scan(&active)
	if err != nil {
		return false
	}
	return active
}

func (u *User) Activate(db *sql.DB) bool {
	_, err := db.Exec("UPDATE auth SET active = true WHERE username = ?", u.Username)
	if err != nil {
		return false
	}
	return true
}

func (u *User) GetField(db *sql.DB, field string) (data string, err error) {
	err = db.QueryRow("SELECT "+field+" FROM auth WHERE username = ?", u.Username).Scan(&data)
	return data, err
}

func (u *User) GetFields(db *sql.DB, fields []string) (data []string, err error) {
	query := "SELECT "
	for i, field := range fields {
		if i == len(fields)-1 {
			query += field
		} else {
			query += field + ", "
		}
	}
	query += " FROM auth WHERE username = ?"
	err = db.QueryRow(query, u.Username).Scan(&data)
	return data, err
}

func (u *User) UpdateField(db *sql.DB, field string, value string) bool {
	_, err := db.Exec(fmt.Sprintf("UPDATE auth SET %s = ? WHERE username = ?", field), value, u.Username)
	if err != nil {
		return false
	}
	return true
}

func (u *User) Validate(db *sql.DB, ctx context.Context) bool {
	cache := connection.Cache
	password, err := cache.Get(ctx, fmt.Sprintf(":validate:%s", u.Username)).Result()
	if err == nil && len(password) > 0 {
		return u.Password == password
	}

	var count int
	err = db.QueryRow("SELECT COUNT(*) FROM auth WHERE username = ? AND password = ?", u.Username, u.Password).Scan(&count)
	if err != nil || count == 0 {
		return false
	}
	cache.Set(ctx, fmt.Sprintf(":validate:%s", u.Username), u.Password, 30*time.Minute)
	return true
}
