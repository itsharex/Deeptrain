import time
import jwt
from django.apps import apps
from DjangoWebsite.settings import SECRET_KEY, TOKEN_VALID_TIME


def generate_token(username, password) -> str:
    return jwt.encode({"username": username, "password": password, "time": time.time()},
                      key=SECRET_KEY,
                      algorithm='HS256')


def decode_token(token: str) -> dict:
    return jwt.decode(token,
                      key=SECRET_KEY,
                      algorithms='HS256')


def validate_token(token: str):
    """
    :param token: jwt token
    :return: User instance or None
    """
    try:
        val = decode_token(token)
        username, password, generate_time = val.get("username"), val.get("password"), val.get("time")
        if time.time() - generate_time > TOKEN_VALID_TIME:
            return
        query = apps.get_model("user", "User").objects.filter(username=username, password=password)
        if not query.exists():
            return

        return query.first()
    except jwt.exceptions.DecodeError:
        return
