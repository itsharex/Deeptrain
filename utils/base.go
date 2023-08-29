package utils

import (
	"encoding/json"
	"os"
	"strconv"
	"strings"
	"time"
)

func Contains[T comparable](value T, slice []T) bool {
	for _, item := range slice {
		if item == value {
			return true
		}
	}
	return false
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
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

func Fix(n int, length int) string {
	// 000034
	s := strconv.Itoa(n)
	if len(s) >= length {
		return s
	}
	return strings.Repeat("0", length-len(s)) + s
}

func GetPrefixArray(s string, p []string) string {
	for _, v := range p {
		if strings.HasPrefix(s, v) {
			return v
		}
	}
	return ""
}

func GetSuffixArray(s string, p []string) string {
	for _, v := range p {
		if strings.HasSuffix(s, v) {
			return v
		}
	}
	return ""
}

func GetPrefixMap[T comparable](s string, p map[string]T) *T {
	for k, v := range p {
		if strings.HasPrefix(s, k) {
			return &v
		}
	}
	return nil
}

func GetSuffixMap[T comparable](s string, p map[string]T) *T {
	for k, v := range p {
		if strings.HasSuffix(s, k) {
			return &v
		}
	}
	return nil
}

func ConvertTime(t []uint8) *time.Time {
	val, err := time.Parse("2006-01-02 15:04:05", string(t))
	if err != nil {
		return nil
	}
	return &val
}

func MapToStruct(m interface{}, s interface{}) error {
	b, err := json.Marshal(m)
	if err != nil {
		return err
	}
	return json.Unmarshal(b, s)
}

func FileExists(filepath string) bool {
	_, err := os.Stat(filepath)
	return err == nil || os.IsExist(err)
}

func ParseInt(s string, def int) int {
	val, err := strconv.Atoi(s)
	if err != nil {
		return def
	}
	return val
}
