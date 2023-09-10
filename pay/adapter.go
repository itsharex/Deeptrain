package pay

import (
	"database/sql"
	"deeptrain/auth"
	"deeptrain/utils"
	"fmt"
	"github.com/go-pay/gopay/pkg/util"
	"time"
)

func NewOrderExec(way string, db *sql.DB, user *auth.User, amount float32) (string, error) {
	// return 32-bit id
	// support Alipay, WeChat pay.
	date := time.Now().Format("20060102150405")
	id := fmt.Sprintf("%s%s", date, utils.Sha2Encrypt(fmt.Sprintf("%s%s%s", way, date, user.Username))[:16]) + util.RandomNumber(2)

	_, err := db.Exec(`
		INSERT INTO payment_log (user_id, order_id, amount, payment_type)
		VALUES (?, ?, ?, ?)
	`, user.GetID(db), id, amount, way)
	if err != nil {
		return "", err
	}

	return id, nil
}

func FinishPayment(db *sql.DB, id string, amount string) error {
	_, err := db.Exec(`
		UPDATE payment_log
		SET payment_status = TRUE
		WHERE order_id = ? AND amount = ? AND payment_status = FALSE
	`, id, amount)
	if err != nil {
		return err
	}

	user := auth.User{}
	err = db.QueryRow(`SELECT user_id FROM payment_log WHERE order_id = ?`, id).Scan(&user.ID)
	if err != nil {
		return err
	}

	// create payment if not exists
	_, err = db.Exec(`
		INSERT INTO payment (user_id, amount, total_amount)
		VALUES (?, ?, ?)
		ON DUPLICATE KEY UPDATE amount = amount + ?, total_amount = total_amount + ?
	`, user.ID, amount, amount, amount, amount)
	if err != nil {
		return err
	}

	return nil
}
