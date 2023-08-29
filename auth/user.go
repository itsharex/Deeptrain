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
	ID       int
}

func IsUserExists(db *sql.DB, username string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM auth WHERE username = ?", username).Scan(&count)
	if err != nil {
		return true
	}
	return count > 0
}

func IsEmailExists(db *sql.DB, email string) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM auth WHERE email = ?", email).Scan(&count)
	if err != nil {
		return true
	}
	return count > 0
}

func IsUserAdmin(db *sql.DB, username string) bool {
	var isAdmin bool
	err := db.QueryRow("SELECT is_admin FROM auth WHERE username = ?", username).Scan(&isAdmin)
	if err != nil {
		return false
	}
	return isAdmin
}

func GetUserFromEmail(db *sql.DB, email string) *User {
	user := &User{}
	err := db.QueryRow("SELECT username, password, email, active, is_admin FROM auth WHERE email = ?", email).Scan(
		&user.Username, &user.Password, &user.Email, &user.Active, &user.IsAdmin,
	)
	if err != nil {
		return nil
	}
	return user
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

func (u *User) GetID(db *sql.DB) int {
	var id int
	err := db.QueryRow("SELECT id FROM auth WHERE username = ?", u.Username).Scan(&id)
	if err != nil {
		return -1
	}
	return id
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

func (u *User) IsCert(db *sql.DB, ctx context.Context) bool {
	cache := connection.Cache
	cert, err := cache.Get(ctx, fmt.Sprintf(":cert:%s", u.Username)).Result()
	if err == nil && len(cert) > 0 {
		return cert == "true"
	}

	var status bool
	err = db.QueryRow("SELECT cert_status FROM cert WHERE user_id = ?", u.GetID(db)).Scan(&status)
	if err != nil || !status {
		return false
	}
	cache.Set(ctx, fmt.Sprintf(":cert:%s", u.Username), "true", 5*time.Second)
	return true
}

func (u *User) IsTeenager(db *sql.DB, ctx context.Context) bool {
	if !u.IsCert(db, ctx) {
		return false
	}

	cache := connection.Cache
	teenager, err := cache.Get(ctx, fmt.Sprintf(":teenager:%s", u.Username)).Result()
	if err == nil && len(teenager) > 0 {
		return teenager == "true"
	}

	var birthDate string
	err = db.QueryRow("SELECT birth_date FROM cert WHERE user_id = ?", u.GetID(db)).Scan(&birthDate)
	if err != nil {
		return false
	}

	birth, err := time.Parse("2006-01-02", birthDate)
	if err != nil {
		return false
	}

	now := time.Now()
	age := now.Year() - birth.Year()
	if now.Month() < birth.Month() || (now.Month() == birth.Month() && now.Day() < birth.Day()) {
		age--
	}

	if age < 18 {
		cache.Set(ctx, fmt.Sprintf(":teenager:%s", u.Username), "true", 5*time.Second)
		return true
	}
	cache.Set(ctx, fmt.Sprintf(":teenager:%s", u.Username), "false", 5*time.Second)
	return false
}
