from hashlib import md5
from typing import Tuple, Union

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse
from model.models import *
import webtoken

spec_string = "\'\"<>~`?/\\*&^%$#@!:"  # 抵御大部分SQL注入, emoji导致长度识别错位
default_detail = "nothing..."


def encode_md5(code: str) -> "32x str":
    return md5(code.encode("utf-8")).hexdigest()  # [8:-8] 16x


def regular_string(string: str) -> bool:
    return not any(map(lambda s: s in spec_string, string))


def is_available_username(username: str) -> bool:
    return 3 <= len(username) <= 12 and regular_string(username)


def is_available_password(password: str) -> bool:
    return 6 <= len(password) <= 14 and regular_string(password)


def login(username: str, password: str) -> Tuple[bool, str]:
    if not is_available_username(username):
        return False, "账户名格式错误, 请勿输入非法字符!"
    if not is_available_password(password):
        return False, "密码格式错误, 请勿输入非法字符!"

    Objs = User.objects.filter(username=username)

    if len(Objs) == 0:
        return False, "账户不存在!"
    else:
        user: User = Objs[0]
        if user.password == encode_md5(password):
            return True, "登录成功!"
        else:
            return False, "账户名 / 密码错误!"


def register(username: str, password: str, re_password: str) -> (bool, str):
    if not is_available_username(username):
        return False, "账户名格式错误, 请勿输入非法字符!"
    if not is_available_password(password):
        return False, "密码格式错误, 请勿输入非法字符!"
    if not password == re_password:
        return False, "校验密码错误!"
    if User.objects.filter(username=username):
        return False, "账户已存在!"

    obj = User.objects.create(username=username, password=encode_md5(password))
    Profile.objects.create(user_bind=obj, detail="", identity=0)
    return True, "创建成功!"


def login_with_cookie_or_token(username: str, md5_password: str) -> bool:
    resp = User.objects.filter(username=username)
    return resp.first().password == md5_password if resp else False


def get_userinfo_from_cookies(request: WSGIRequest) -> Tuple[str, str]:
    return request.COOKIES.get("username", str()), request.COOKIES.get("password", str())


def could_login_by_cookies(request: WSGIRequest) -> bool:
    return login_with_cookie_or_token(*get_userinfo_from_cookies(request))


def set_cookies(response: HttpResponse, **kwargs):
    for key, value in kwargs.items():
        response.set_cookie(key, value, max_age=60 * 60 * 24 * 30 * 2)  # max_age: second. <2 months>
    return response


def delete_cookies(response: HttpResponse, *args):
    for item in args:
        response.delete_cookie(item)
    return response


def get_user_from_name(username: str) -> User:
    """Registered(RAISE if it is empty or >1.)"""
    return User.objects.get(username=username)


def get_user_from_id(uid: int) -> Union[User, None]:
    Query = User.objects.filter(id=uid)
    return Query.first() if Query else None


def get_profile_from_user(userObj: User) -> Profile:
    return Profile.objects.get(user_bind=userObj)


def update_data_from_user(userObj: User, detail=None, identity=None) -> Union[int, str, None]:
    """2 channels:
        <1. change detail>
        <2. change identity>
    """
    if detail and isinstance(detail, str):
        detail = detail.strip()
        if detail != default_detail and detail != get_profile_from_user(userObj).get_data(default_detail)[0]:
            Profile.objects.filter(user_bind=userObj).update(detail=detail)
        return get_profile_from_user(userObj).get_data(default_detail)[0]
    elif isinstance(identity, int):  # User<identity>: 0
        Profile.objects.filter(user_bind=userObj).update(identity=identity)
        return identity
    return None


def get_data_from_username(username: str) -> [User, (Profile.detail, Profile.identity)]:
    obj = get_user_from_name(username)
    return obj, get_profile_from_user(obj).get_data(default_detail=default_detail)


def get_data_from_uid(uid: int) -> [(User, [Profile.detail, Profile.identity]), None]:
    obj = get_user_from_id(uid)
    return (obj, get_profile_from_user(obj).get_data(default_detail=default_detail)) if obj else None


webtoken_encode = webtoken.encode


def webtoken_encode_from_user(user: User) -> str:
    return webtoken_encode(user.username, user.password)


def webtoken_validate(token: str) -> Tuple[bool, str]:
    username, password = webtoken.decode(token)
    return login_with_cookie_or_token(username, password), username
