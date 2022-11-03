from typing import List, Tuple

import jwt
from DjangoWebsite.settings import SECRET_KEY as SALT


def encode(username, password) -> str:
    return jwt.encode({"username": username, "password": password},
                      key=SALT,
                      algorithm='HS256')


def _decode(token: str) -> dict:
    return jwt.decode(token,
                      key=SALT,
                      algorithms='HS256')


def decode(token: str) -> Tuple[str, str]:
    resp: dict = _decode(token)
    return resp["username"], resp["password"]
