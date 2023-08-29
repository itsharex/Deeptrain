package auth

import (
	"deeptrain/utils"
	"github.com/gin-gonic/gin"
	"net/http"
)

func PackageView(c *gin.Context) {
	user := c.MustGet("user").(string)
	if user == "" {
		c.JSON(http.StatusOK, gin.H{
			"status": false,
			"error":  "unauthorized access",
		})
		return
	}

	instance := User{
		Username: user,
	}
	db := utils.GetDBFromContext(c)

	c.JSON(http.StatusOK, gin.H{
		"status": true,
		"data": gin.H{
			"cert":     instance.IsCert(db, c),
			"minority": instance.IsTeenager(db, c),
		},
	})
}
