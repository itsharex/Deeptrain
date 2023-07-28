package oauth

import (
	"database/sql"
	"deeptrain/auth"
	"time"
)

type OUser struct {
	ID         int
	UserID     int
	Provider   string
	ProviderID string
	CreatedAt  time.Time
}

func IsOAuthExist(db *sql.DB, provider string, providerID int) bool {
	var count int
	err := db.QueryRow("SELECT COUNT(*) FROM oauth WHERE provider = ? AND provider_id = ?", provider, providerID).Scan(&count)
	if err != nil {
		return false
	}
	return count > 0
}

func GetOAuthUserID(db *sql.DB, provider string, providerID int) int {
	var id int
	err := db.QueryRow("SELECT user_id FROM oauth WHERE provider = ? AND provider_id = ?", provider, providerID).Scan(&id)
	if err != nil {
		return 0
	}
	return id
}

func GetOAuthUser(db *sql.DB, provider string, providerID int) *OUser {
	var instance OUser
	err := db.QueryRow("SELECT * FROM oauth WHERE provider = ? AND provider_id = ?", provider, providerID).Scan(&instance.ID, &instance.UserID, &instance.Provider, &instance.ProviderID, &instance.CreatedAt)
	if err != nil {
		return nil
	}
	return &instance
}

func GetUserFromOAuth(db *sql.DB, provider string, providerID int) *auth.User {
	id := GetOAuthUserID(db, provider, providerID)
	if id == 0 {
		return nil
	}

	var instance auth.User
	err := db.QueryRow("SELECT * FROM auth WHERE id = ?", id).Scan(&instance.ID, &instance.Username, &instance.Password, &instance.Email, &instance.Active, &instance.CreateAt, &instance.IsAdmin)
	if err != nil {
		return nil
	}

	return &instance
}
