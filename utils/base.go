package utils

import "strings"

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
