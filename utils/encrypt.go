package utils

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"io"
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

func HmacEncrypt(key string, data string) string {
	mac := hmac.New(sha256.New, []byte(key))
	mac.Write([]byte(data))
	return hex.EncodeToString(mac.Sum(nil))
}

func HmacCompare(key string, data string, encrypted string) bool {
	return HmacEncrypt(key, data) == encrypted
}

func AES256Encrypt(key string, data string) (string, error) {
	text := []byte(data)
	block, err := aes.NewCipher([]byte(key))
	if err != nil {
		return "", err
	}

	iv := make([]byte, aes.BlockSize)
	if _, err := io.ReadFull(rand.Reader, iv); err != nil {
		return "", err
	}

	encryptor := cipher.NewCFBEncrypter(block, iv)

	ciphertext := make([]byte, len(text))
	encryptor.XORKeyStream(ciphertext, text)
	return hex.EncodeToString(ciphertext), nil
}

func AES256Decrypt(key string, data string) (string, error) {
	ciphertext, err := hex.DecodeString(data)
	if err != nil {
		return "", err
	}

	block, err := aes.NewCipher([]byte(key))
	if err != nil {
		return "", err
	}

	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	decryptor := cipher.NewCFBDecrypter(block, iv)
	plaintext := make([]byte, len(ciphertext))
	decryptor.XORKeyStream(plaintext, ciphertext)

	return string(plaintext), nil
}
