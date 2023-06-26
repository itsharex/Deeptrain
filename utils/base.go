package utils

import (
	"database/sql"
	"github.com/gin-gonic/gin"
)

func Contains[T comparable](value T, slice []T) bool {
	for _, item := range slice {
		if item == value {
			return true
		}
	}
	return false
}

func Sum[N int | float64](m []N) N {
	total := N(0)
	for _, v := range m {
		total += v
	}
	return total
}

func All(condition ...bool) bool {
	for _, c := range condition {
		if !c {
			return false
		}
	}
	return true
}

func Any(condition ...bool) bool {
	for _, c := range condition {
		if c {
			return true
		}
	}
	return false
}

func Max[N int | float64](m []N) N {
	max := m[0]
	for _, v := range m {
		if v > max {
			max = v
		}
	}
	return max
}

func Min[N int | float64](m []N) N {
	min := m[0]
	for _, v := range m {
		if v < min {
			min = v
		}
	}
	return min
}

func GetDBFromContext(c *gin.Context) *sql.DB {
	return c.MustGet("db").(*sql.DB)
}
