package connection

import (
	"context"
	"fmt"
	"github.com/go-redis/redis/v8"
	"github.com/spf13/viper"
	"log"
)

var cache *redis.Client

func ConnectRedis() *redis.Client {
	// connect to redis
	cache = redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%d", viper.GetString("redis.host"), viper.GetInt("redis.port")),
		Password: viper.GetString("redis.password"),
		DB:       viper.GetInt("redis.db"),
	})
	_, err := cache.Ping(context.Background()).Result()

	if err != nil {
		log.Fatalln("Failed to connect to Redis server: ", err)
	} else {
		log.Println("Connected to Redis server successfully")
	}

	if viper.GetBool("flush") {
		cache.FlushAll(context.Background())
		log.Println("Flushed all cache")
	}

	return cache
}
