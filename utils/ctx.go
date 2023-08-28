package utils

import (
	"database/sql"
	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v8"
	"strings"
)

func GetDBFromContext(c *gin.Context) *sql.DB {
	return c.MustGet("db").(*sql.DB)
}

func GetCacheFromContext(c *gin.Context) *redis.Client {
	return c.MustGet("cache").(*redis.Client)
}

func GetUAFromContext(c *gin.Context) string {
	return c.GetHeader("User-Agent")
}

func GetIPFromContext(c *gin.Context) string {
	return c.ClientIP()
}

func IsMobile(ua string) bool {
	return strings.Contains(ua, "Mobile")
}
