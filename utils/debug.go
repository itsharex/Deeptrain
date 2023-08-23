package utils

import "fmt"

func Debug[T comparable](v T) T {
	fmt.Println(v)
	return v
}

func Debugf[T comparable](format string, v T) T {
	fmt.Printf(format, v)
	return v
}

func TryPanic(err error) {
	if err != nil {
		panic(err)
	}
}

func TryWithPanic[T any](v T, err error) T {
	if err != nil {
		panic(err)
	}
	return v
}
