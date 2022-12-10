from typing import Tuple, Union
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from user.models import *
import webtoken
from django.contrib import auth


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
    user = User.objects.get(id=userObj.id)
    return Profile.objects.get(user=user)


def get_data_from_username(username: str) -> [User, (Profile.detail, Profile.identity)]:
    obj = get_user_from_name(username)
    return obj, get_profile_from_user(obj).get_data()


def get_data_from_uid(uid: int) -> [(User, [Profile.detail, Profile.identity]), None]:
    obj = get_user_from_id(uid)
    return (obj, get_profile_from_user(obj).get_data()) if obj else None


webtoken_encode = webtoken.encode


def webtoken_encode_from_user(user: User) -> str:
    return webtoken_encode(user.username, user.password)


def webtoken_validate(token: str) -> Tuple[bool, str]:
    username, password = webtoken.decode(token)
    return login_with_cookie_or_token(username, password), username
