package auth

import (
	"database/sql"
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

func RequireAuth(c *gin.Context) *User {
	user := c.MustGet("user")
	if user == "" {
		c.JSON(http.StatusUnauthorized, gin.H{"status": false, "reason": "You are not logged in."})
		c.Abort()
		return nil
	}
	return &User{
		Username: user.(string),
	}
}

func RequireActive(c *gin.Context) *User {
	user := RequireAuth(c)
	if user == nil {
		return nil
	}
	if !user.IsActive(c.MustGet("db").(*sql.DB)) {
		c.JSON(http.StatusUnauthorized, gin.H{"status": false, "reason": "Your account is not activated."})
		c.Abort()
		return nil
	}
	return user
}

func RequireQuery(c *gin.Context, key string) string {
	value := strings.TrimSpace(c.Query(key))
	if value == "" {
		c.JSON(http.StatusBadRequest, gin.H{"status": false, "reason": "Invalid query."})
		c.Abort()
		return ""
	}
	return value
}

func IsLogin(c *gin.Context) string {
	return c.MustGet("user").(string)
}

func IsActive(c *gin.Context) *User {
	user := c.MustGet("user")
	if user == "" {
		return nil
	}

	instance := &User{
		Username: user.(string),
	}

	if instance.IsActive(c.MustGet("db").(*sql.DB)) {
		return instance
	}
	return nil
}
