package middleware

import (
	"deeptrain/auth"
	"github.com/gin-gonic/gin"
	"strings"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		raw := strings.TrimSpace(c.GetHeader("Authorization"))
		if raw != "" {
			if token := auth.ParseToken(raw); token != nil {
				c.Set("user", token.Username)
			}
			c.Next()
		}
		c.Set("user", "")
		c.Next()
	}
}
