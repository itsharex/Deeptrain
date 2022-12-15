from django import forms
from django.contrib import auth
from hcaptcha.fields import hCaptchaField as CaptchaField
from django.core.exceptions import ValidationError
from typing import *

from user.models import User, Profile

spec_string = "\'\"<>~`?/\\*&^%$#@!:"  # 抵御大部分SQL注入, emoji导致长度识别错位
default_detail = "nothing..."


def regular_string(string: str) -> bool:
    return not any(map(lambda s: s in spec_string, string))


def is_available_username(username: str) -> bool:
    return 3 <= len(username) <= 12 and regular_string(username)


def is_available_password(password: str) -> bool:
    return 6 <= len(password) <= 14 and regular_string(password)


class UserLoginForm(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=12,
        label="username",
        error_messages={
            "min_length": "账户名不能小于3位, 请输入3~12位账户名",
            "max_length": "账户名不能大于12位, 请输入3~12位账户名",
            "required": "请输入您的账户名"
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": "账户",
                "value": ""
            }
        )
    )

    password = forms.CharField(
        min_length=6, max_length=14,
        label="password",
        error_messages={
            "required": "请输入密码",
            "min_length": "密码不能小于6位, 请输入6~14位密码",
            "max_length": "密码不能大于14位, 请输入6~14位密码"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "密码",
                "value": ""
            }
        )
    )

    captcha = CaptchaField(
        label="captcha",
        error_messages={
            "required": "请输入验证码",
            "invalid": "验证码输入错误"
        },
    )

    user: User

    def clean(self):
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)
        username, password = self.cleaned_data.get("username"), self.cleaned_data.get("password")
        if not is_available_username(username):
            raise ValidationError("账户名格式错误, 请勿输入非法字符!")
        if not is_available_password(password):
            raise ValidationError("密码格式错误, 请勿输入非法字符!")
        self.user = auth.authenticate(username=username, password=password)
        if not self.user:
            raise ValidationError("登录错误!")

        return super().clean()

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]


class UserRegisterForm(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=12,
        label="username",
        error_messages={
            "min_length": "账户名不能小于3位, 请输入3~12位账户名",
            "max_length": "账户名不能大于12位, 请输入3~12位账户名",
            "required": "请输入您的账户名"
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": "账户",
                "value": ""
            }
        )
    )

    password = forms.CharField(
        min_length=6, max_length=14,
        label="password",
        error_messages={
            "required": "请输入密码",
            "min_length": "密码不能小于6位, 请输入6~14位密码",
            "max_length": "密码不能大于14位, 请输入6~14位密码"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "密码",
                "value": ""
            }
        )
    )

    re_password = forms.CharField(
        min_length=6, max_length=14,
        label="re-password",
        error_messages={
            "required": "请再次输入密码",
            "min_length": "密码不能小于6位, 请输入6~14位密码",
            "max_length": "密码不能大于14位, 请输入6~14位密码"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "再次输入密码",
                "value": ""
            }
        )
    )

    captcha = CaptchaField(
        label="captcha",
        required=True,
        error_messages={
            "required": "请输入验证码",
            "invalid": "验证码输入错误"
        },
    )

    user: User
    country: str

    def clean(self):
        super().clean()
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)
        username, password, re_password = \
            self.cleaned_data.get("username"), self.cleaned_data.get("password"), self.cleaned_data.get("re_password")
        if not is_available_username(username):
            raise ValidationError("账户名格式错误, 请勿输入非法字符!")
        if not is_available_password(password):
            raise ValidationError("密码格式错误, 请勿输入非法字符!")
        if not password == re_password:
            raise ValidationError("两次输入密码不一致!")
        if User.objects.filter(username=username).exists():
            raise ValidationError("用户已存在!")

        self.user = User.objects.create_user(username=username, password=password, identity=0, country=self.country)
        Profile.objects.create(user=self.user, profile="")
        return self.cleaned_data

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]
