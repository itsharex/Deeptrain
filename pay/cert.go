package pay

import (
	"context"
	"database/sql"
	"deeptrain/auth"
	"deeptrain/utils"
	"errors"
	"fmt"
	"github.com/go-pay/gopay"
	"github.com/spf13/viper"
	"regexp"
	"strconv"
	"time"
)

func ValidateName(name string) bool {
	return len([]rune(name)) >= 2
}

func ValidateNo(no string) bool {
	pattern := `^(\d{17}[\dXx])|(\d{15})$`
	matched, _ := regexp.MatchString(pattern, no)
	if !matched {
		return false
	}

	code := []string{"1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"}

	weights := []int{7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2}
	checker := 0
	for i, char := range no[:17] {
		digit, err := strconv.Atoi(string(char))
		if err != nil {
			return false
		}
		checker += digit * weights[i]
	}

	remainder := checker % 11
	if no[17:] != code[remainder] {
		return false
	}

	return true
}

func HideName(name string) string {
	runes := []rune(name)
	if len(runes) == 2 {
		runes[1] = '*'
		return string(runes)
	}
	for i := 1; i < len(runes)-1; i++ {
		runes[i] = '*'
	}
	return string(runes)
}

func HideNo(no string) string {
	return no[:4] + "***********" + no[15:]
}

func GetBirthDate(no string) time.Time {
	var date time.Time
	if len(no) == 18 {
		date, _ = time.Parse("20060102", no[6:14])
	} else {
		date, _ = time.Parse("20060102", "19"+no[6:12])
	}
	return date
}

func GetAge(no string) int {
	date := GetBirthDate(no)
	return time.Now().Year() - date.Year()
}

func IsAdult(no string) bool {
	return GetAge(no) >= 18
}

func IsMale(no string) bool {
	return no[16]%2 == 1
}

func IsFemale(no string) bool {
	return no[16]%2 == 0
}

func InitCertRequest(id, name, no string) (string, error) {
	instance := make(gopay.BodyMap)
	instance.Set("outer_order_no", id)
	instance.Set("biz_code", "FACE")
	instance.Set("identity_param", map[string]string{
		"identity_type": "CERT_INFO",
		"cert_type":     "IDENTITY_CARD",
		"cert_name":     name,
		"cert_no":       no,
	})
	instance.Set("merchant_config", map[string]string{
		"return_url": viper.GetString("pay.cert.return_url"),
	})

	ctx := context.Background()
	resp, err := aliClient.UserCertifyOpenInit(ctx, instance)
	if err != nil {
		fmt.Println(err.Error())
		return "", err
	}

	return resp.Response.CertifyId, nil
}

func CreateCertRequest(id string) (string, error) {
	instance := make(gopay.BodyMap)
	instance.Set("certify_id", id)

	ctx := context.Background()
	url, err := aliClient.UserCertifyOpenCertify(ctx, instance)
	if err != nil {
		fmt.Println(err.Error())
		return "", err
	}

	return url, nil
}

func VerifyCertRequest(id string) bool {
	instance := make(gopay.BodyMap)
	instance.Set("certify_id", id)

	ctx := context.Background()
	resp, err := aliClient.UserCertifyOpenQuery(ctx, instance)
	if err != nil {
		fmt.Println(err.Error())
		return false
	}

	return resp.Response.Passed == "T"
}

func GenerateCertHash(name, no string) string {
	// return 32-bit order id
	t := time.Now().Format("20060102150405")
	r := utils.GenerateCode(6)
	return utils.Md5Encrypt(name + no + t)[:26] + r
}

func IsNumberExist(db *sql.DB, no string) bool {
	var count int
	err := db.QueryRow(`SELECT COUNT(*) FROM cert WHERE cert_number = ? AND cert_status = TRUE`, no).Scan(&count)
	if err != nil {
		return false
	}

	return count > 0
}

func HasValidCert(db *sql.DB, user *auth.User) bool {
	var status bool
	err := db.QueryRow(`SELECT cert_status FROM cert WHERE user_id = ?`, user.GetID(db)).Scan(&status)
	if err != nil {
		return false
	}

	return status
}

func RefreshCert(db *sql.DB, user *auth.User) bool {
	if HasValidCert(db, user) {
		return true
	}

	var no, id string
	err := db.QueryRow(`SELECT verify_id, cert_number FROM cert WHERE user_id = ?`, user.GetID(db)).Scan(&id, &no)
	if err != nil {
		return false
	}

	if !VerifyCertRequest(id) {
		return false
	}

	if IsNumberExist(db, no) {
		return false
	}

	_, err = db.Exec(`UPDATE cert SET cert_status = TRUE WHERE user_id = ?`, user.GetID(db))
	if err != nil {
		return false
	}

	return true
}

func CreateOrUpdateCert(db *sql.DB, user *auth.User, name, no, verifyId string) error {
	if HasValidCert(db, user) {
		return errors.New("already has valid cert")
	}

	if IsNumberExist(db, no) {
		return errors.New("identity number already exists")
	}

	_, err := db.Exec(`
		INSERT INTO cert (user_id, verify_id, cert_name, cert_number, cert_type, cert_status, birth_date)
		VALUES (?, ?, ?, ?, ?, ?, ?)
		ON DUPLICATE KEY UPDATE
		verify_id = VALUES(verify_id),
		cert_name = VALUES(cert_name),
		cert_number = VALUES(cert_number),
		cert_type = VALUES(cert_type),
		cert_status = VALUES(cert_status),
		birth_date = VALUES(birth_date)
	`, user.GetID(db), verifyId, name, no, 0, false, GetBirthDate(no))

	return err
}

func NewCertRequest(db *sql.DB, user *auth.User, name, no string) (string, error) {
	if HasValidCert(db, user) {
		return "", errors.New("already has valid cert")
	}

	if !ValidateName(name) {
		return "", errors.New("invalid name")
	}

	if !ValidateNo(no) {
		return "", errors.New("invalid identity number")
	}

	id := GenerateCertHash(name, no)
	cert, err := InitCertRequest(id, name, no)
	if err != nil {
		return "", fmt.Errorf("failed to initialize cert request: %s", err)
	}

	uri, err := CreateCertRequest(cert)
	if err != nil {
		return "", fmt.Errorf("failed to create cert request: %s", err)
	}

	if err := CreateOrUpdateCert(db, user, name, no, cert); err != nil {
		return "", fmt.Errorf("failed to create cert: %s", err)
	}

	return uri, nil
}

func HasRecord(db *sql.DB, user *auth.User) bool {
	var count int
	err := db.QueryRow(`SELECT COUNT(*) FROM cert WHERE user_id = ?`, user.GetID(db)).Scan(&count)
	if err != nil {
		return false
	}

	return count > 0
}

func GetCert(db *sql.DB, user *auth.User) (name string, no string, id string, err error) {
	if err = db.QueryRow(`SELECT cert_name, cert_number, verify_id FROM cert WHERE user_id = ?`, user.GetID(db)).Scan(&name, &no, &id); err != nil {
		return "", "", "", err
	}

	return HideName(name), HideNo(no), id, nil
}
