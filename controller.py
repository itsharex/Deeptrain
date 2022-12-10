from typing import Tuple, Union
from user.models import *
import webtoken


def login_with_cookie_or_token(username: str, md5_password: str) -> bool:
    resp = User.objects.filter(username=username)
    return resp.first().password == md5_password if resp else False


def webtoken_validate(token: str) -> Tuple[bool, str]:
    username, password = webtoken.decode(token)
    return login_with_cookie_or_token(username, password), username
