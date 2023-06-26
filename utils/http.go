package utils

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
)

func Http(uri string, method string, ptr interface{}, headers map[string]string, body io.Reader) (err error) {
	req, err := http.NewRequest(method, uri, body)
	if err != nil {
		return err
	}
	for key, value := range headers {
		req.Header.Set(key, value)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}

	defer resp.Body.Close()

	if err = json.NewDecoder(resp.Body).Decode(ptr); err != nil {
		return err
	}
	return nil
}

func Get(uri string, headers map[string]string) (data interface{}, err error) {
	err = Http(uri, http.MethodGet, &data, headers, nil)
	return data, err
}

func Post(uri string, headers map[string]string, body interface{}) (data interface{}, err error) {
	var form io.Reader
	if buffer, err := json.Marshal(body); err == nil {
		form = bytes.NewBuffer(buffer)
	}
	err = Http(uri, http.MethodPost, &data, headers, form)
	return data, err
}
