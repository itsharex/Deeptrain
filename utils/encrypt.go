package utils

import (
	"crypto/sha256"
	"encoding/hex"
)

func Sha2Encrypt(raw string) string {
	hash := sha256.Sum256([]byte(raw))
	return hex.EncodeToString(hash[:])
}
