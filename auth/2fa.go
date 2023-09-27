package auth

import (
	"database/sql"
	"deeptrain/utils"
	"errors"
	"github.com/pquerna/otp"
	"github.com/pquerna/otp/totp"
)

func Generate2FAKey(user *User) (*otp.Key, error) {
	return totp.Generate(totp.GenerateOpts{
		Issuer:      "DeepTrain Account",
		AccountName: user.Username,
		Period:      30,
	})
}

func Verify2FAKey(secret string, code string) bool {
	return totp.Validate(code, secret)
}

func (u *User) Generate2FA(db *sql.DB) (string, error) {
	if u.Is2FAEnabled(db) {
		return "", errors.New("2FA is already enabled")
	}
	secret, err := Generate2FAKey(u)
	if err != nil {
		return "", err
	}
	_, err = db.Exec(`
		INSERT INTO factor (user_id, secret, enable) VALUES (?, ?, ?)
		ON DUPLICATE KEY UPDATE secret = ?, enable = ?
	`, u.GetID(db), secret.Secret(), false, secret.Secret(), false)
	if err != nil {
		return "", err
	}
	return utils.GetQRCode(secret.Secret(), secret.URL()), nil
}

func (u *User) Verify2FA(db *sql.DB, code string) bool {
	var secret string
	err := db.QueryRow("SELECT secret FROM factor WHERE user_id = ?", u.GetID(db)).Scan(&secret)
	if err != nil {
		return false
	}
	return Verify2FAKey(secret, code)
}

func (u *User) Activate2FA(db *sql.DB, code string) error {
	if u.Is2FAEnabled(db) {
		return errors.New("2FA is already enabled")
	}
	if !u.Verify2FA(db, code) {
		return errors.New("invalid 2FA code, please check if the code is expired or not correct")
	}
	_, err := db.Exec("UPDATE factor SET enable = TRUE WHERE user_id = ?", u.GetID(db))
	if err != nil && !errors.Is(err, sql.ErrNoRows) {
		return err
	}
	return nil
}

func (u *User) Disable2FA(db *sql.DB) error {
	if !u.Is2FAEnabled(db) {
		return errors.New("2FA is already disabled")
	}
	_, err := db.Exec("UPDATE factor SET enable = FALSE WHERE user_id = ?", u.GetID(db))
	if err != nil && !errors.Is(err, sql.ErrNoRows) {
		return err
	}
	return nil
}

func (u *User) Is2FAEnabled(db *sql.DB) bool {
	var enable bool
	err := db.QueryRow("SELECT enable FROM factor WHERE user_id = ?", u.GetID(db)).Scan(&enable)
	if err != nil {
		return false
	}
	return enable
}
