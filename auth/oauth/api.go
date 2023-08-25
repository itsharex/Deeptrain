package oauth

import (
	"deeptrain/auth"
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

func ListView(c *gin.Context) {
	user := c.MustGet("user").(string)

	if user == "" {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "invalid token"})
		return
	}

	db := utils.GetDBFromContext(c)
	instance := auth.User{Username: user}

	if !instance.IsActive(db) {
		c.JSON(http.StatusOK, gin.H{"status": false, "error": "user is not active"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"status": true, "data": ListUserOAuth(db, instance.GetID(db))})
}
