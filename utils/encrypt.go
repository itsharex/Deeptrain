package utils

import (
	"crypto/sha256"
	"encoding/hex"
)

func Sha2Encrypt(raw string) string {
	hash := sha256.Sum256([]byte(raw))
	return hex.EncodeToString(hash[:])
}

func Sha2Compare(raw, encrypted string) bool {
	return Sha2Encrypt(raw) == encrypted
}

func Md5Encrypt(raw string) string {
	hash := sha256.Sum256([]byte(raw))
	return hex.EncodeToString(hash[:])
}

func Md5Compare(raw, encrypted string) bool {
	return Md5Encrypt(raw) == encrypted
}
