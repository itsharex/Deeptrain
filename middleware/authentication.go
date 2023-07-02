package middleware

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"strings"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		raw := strings.TrimSpace(c.GetHeader("Authorization"))
		if raw != "" {
			db := utils.GetDBFromContext(c)
			if token := auth.ParseToken(c, db, raw); token != nil {
				c.Set("user", token.Username)
				c.Next()
			}
		}
		c.Set("user", "")
		c.Next()
	}
}
