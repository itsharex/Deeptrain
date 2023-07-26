package auth

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v8"
	"image/color"
	"log"
	"math/rand"
	"os"
	"strings"
	"time"
	"unicode/utf8"
)

const avatarSize = 128

func getBackgroundColor() color.RGBA {
	return color.RGBA{R: uint8(rand.Intn(200)), G: uint8(rand.Intn(200)), B: uint8(rand.Intn(200)), A: 255}
}

func SaveAvatar(username string) {
	first, _ := utf8.DecodeRuneInString(username) // Extract the first rune from the username (UTF-8 safe)

	background := getBackgroundColor()

	var canvas strings.Builder
	canvas.WriteString(fmt.Sprintf(`<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">`, avatarSize, avatarSize))

	canvas.WriteString(fmt.Sprintf(`<rect width="%d" height="%d" style="fill:rgb(%d,%d,%d);" />`, avatarSize, avatarSize, background.R, background.G, background.B))
	canvas.WriteString(fmt.Sprintf(`<text x="%d" y="%d" text-anchor="middle" dominant-baseline="middle" font-family="Arial" font-size="50" fill="white">%s</text>`, avatarSize/2, avatarSize/2+16, string(first)))
	canvas.WriteString("</svg>")

	data := []byte(canvas.String())
	if err := os.WriteFile(fmt.Sprintf("storage/avatar/%s.svg", username), data, 0644); err != nil {
		log.Println(err)
	} else {
		SaveAvatarConfig(username, fmt.Sprintf("%s.svg", username))
	}
}

func SaveAvatarConfig(username, path string) bool {
	if _, err := os.Stat("storage/avatar/config.json"); os.IsNotExist(err) {
		data := []byte("{}")
		if err := os.WriteFile("storage/avatar/config.json", data, 0644); err != nil {
			log.Println(err)
			return false
		}
	}

	var config map[string]string

	data, err := os.ReadFile("storage/avatar/config.json")
	if err != nil {
		log.Println(err)
		return false
	}

	if err := json.Unmarshal(data, &config); err != nil {
		log.Println(err)
		return false
	}

	config[username] = path

	data, err = json.Marshal(config)
	if err != nil {
		log.Println(err)
		return false
	}

	if err := os.WriteFile("storage/avatar/config.json", data, 0644); err != nil {
		log.Println(err)
		return false
	}

	return true
}

func GetAvatarConfigWithCache(c *gin.Context, username string) string {
	cache := c.MustGet("cache").(*redis.Client)
	if value, err := cache.Get(c, fmt.Sprintf("avatar:%s", username)).Result(); err == nil {
		return value
	}

	var config map[string]string
	data, err := os.ReadFile("storage/avatar/config.json")
	if err != nil {
		log.Println(err)
		return ""
	}

	if err := json.Unmarshal(data, &config); err != nil {
		log.Println(err)
		return ""
	}

	cache.Set(c, fmt.Sprintf("avatar:%s", username), config[username], time.Minute*30)
	return config[username]
}

func GetAvatarView(c *gin.Context) {
	username := c.Param("username")
	if len(username) == 0 {
		c.JSON(400, gin.H{"error": "username is required"})
		return
	}

	path := GetAvatarConfigWithCache(c, username)
	if len(path) == 0 {
		db := c.MustGet("db").(*sql.DB)
		if isUserExists(db, username) {
			SaveAvatar(username)
			path = GetAvatarConfigWithCache(c, username)
			c.File(path)
			return
		} else {
			c.JSON(404, gin.H{"error": "avatar not found"})
			return
		}
	}

	c.File(fmt.Sprintf("storage/avatar/%s", path))
}
