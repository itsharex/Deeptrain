from random import choice, random


def generate_code(length=10 ** 3, code_population="asdfjlk;qwertyuiopzxcvbnm,./;'[]1234567890-=`~_+?<>"):
    return "".join([choice(code_population) for _ in range(length)])


def generate_ncode(length=10) -> str:
    return generate_code(length, code_population="0123456789")
