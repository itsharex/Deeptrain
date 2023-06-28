package middleware

import (
	"deeptrain/auth"
	"github.com/gin-gonic/gin"
	"strings"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		raw := strings.TrimSpace(c.GetHeader("Authorization"))
		c.Set("user", auth.ParseToken(raw))
		c.Next()
	}
}
