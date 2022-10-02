import jwt
from DjangoWebsite.settings import SECRET_KEY as salt


def encode(username, password) -> str:
    return jwt.encode({"username": username, "password": password},
                      key=salt,
                      algorithm='HS256')


def _decode(token: str) -> dict:
    return jwt.decode(token,
                      key=salt,
                      algorithms='HS256')


def decode(token: str) -> (str, str):
    resp = _decode(token)
    return resp["username"], resp["password"]
