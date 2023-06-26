package utils

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
