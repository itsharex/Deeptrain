package middleware

import (
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

var allowedOrigins = []string{
	"https://deeptrain.net",
	"https://www.deeptrain.net",
	"https://deeptrain.lightxi.com",
	"https://deeptrain.vercel.app",
	"http://localhost",
	"http://localhost:5173",
}

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		origin := c.Request.Header.Get("Origin")
		if utils.Contains(origin, allowedOrigins) {
			c.Writer.Header().Set("Access-Control-Allow-Origin", origin)
			c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
			c.Writer.Header().Set("Access-Control-Allow-Headers", "Origin, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
			c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
			c.Writer.Header().Set("Access-Control-Max-Age", "7200")

			if c.Request.Method == "OPTIONS" {
				c.AbortWithStatus(http.StatusOK)
				return
			}
		}

		c.Next()
	}
}
