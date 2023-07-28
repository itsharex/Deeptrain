package utils

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"net/url"
)

type PostFormRequest struct {
	Uri    string
	Header map[string]string
	Body   map[string]interface{}
}

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

func PostForm(req PostFormRequest) (data map[string]interface{}, err error) {
	client := &http.Client{}
	form := make(url.Values)
	for key, value := range req.Body {
		form[key] = []string{value.(string)}
	}

	uri, err := url.Parse(req.Uri)
	if err != nil {
		return nil, err
	}
	uri.RawQuery = form.Encode()
	request, err := http.NewRequest("POST", uri.String(), nil)
	if err != nil {
		return nil, err
	}

	for key, value := range req.Header {
		request.Header.Set(key, value)
	}

	res, err := client.Do(request)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	content, err := io.ReadAll(res.Body)
	if err != nil {
		return nil, err
	}

	if err = json.Unmarshal(content, &data); err != nil {
		return nil, err
	}

	return data, nil
}
