from django import forms
from django.contrib import auth
from hcaptcha.fields import hCaptchaField as CaptchaField
from django.core.exceptions import ValidationError
from typing import *

from user.models import User, Profile

spec_string = "\'\"<>~`?/\\*&^%$#@!:"  # 抵御大部分SQL注入, emoji导致长度识别错位, XSS攻击
default_detail = "nothing..."


def regular_string(string: str) -> bool:
    return not any(map(lambda s: s in spec_string, string))


def is_available_username(username: str) -> bool:
    return 3 <= len(username) <= 12 and regular_string(username)


def is_available_password(password: str) -> bool:
    return 6 <= len(password) <= 14 and regular_string(password)


def is_available_profile(profile: str) -> bool:
    return 1 <= len(profile) <= 200


class UserLoginForm(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=12,
        label="username",
        error_messages={
            "min_length": "The user name cannot be smaller than 3 characters. Please enter 3 to 12 characters",
            "max_length": "The user name cannot be larger than 12 characters. Please enter 3 to 12 characters",
            "required": "Please enter your user name"
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": "User name",
                "value": ""
            }
        )
    )

    password = forms.CharField(
        min_length=6, max_length=14,
        label="password",
        error_messages={
            "required": "Please enter your password",
            "min_length": "The password cannot be smaller than 6 characters. Please enter 6 to 14 characters",
            "max_length": "The password cannot be larger than 14 characters. Please enter 6 to 14 characters"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "value": ""
            }
        )
    )

    captcha = CaptchaField(
        label="captcha",
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
        },
    )

    user: User

    def clean(self):
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)
        username, password = self.cleaned_data.get("username"), self.cleaned_data.get("password")
        if not is_available_username(username):
            raise ValidationError("Username format entered wrong! Do not enter illegal characters")
        if not is_available_password(password):
            raise ValidationError("Password format entered wrong! Do not enter illegal characters")
        self.user = auth.authenticate(username=username, password=password)
        if not self.user:
            raise ValidationError("Login error!")

        return super().clean()

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]


class UserRegisterForm(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=12,
        label="username",
        error_messages={
            "min_length": "The user name cannot be smaller than 3 characters. Please enter 3 to 12 characters",
            "max_length": "The user name cannot be larger than 12 characters. Please enter 3 to 12 characters",
            "required": "Please enter your user name"
        },
        widget=forms.TextInput(
            attrs={
                "placeholder": "User name",
                "value": ""
            }
        )
    )

    password = forms.CharField(
        min_length=6, max_length=14,
        label="password",
        error_messages={
            "required": "Please enter your password",
            "min_length": "The password cannot be smaller than 6 characters. Please enter 6 to 14 characters",
            "max_length": "The password cannot be larger than 14 characters. Please enter 6 to 14 characters"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "value": ""
            }
        )
    )

    re_password = forms.CharField(
        min_length=6, max_length=14,
        label="re-password",
        error_messages={
            "required": "Please enter your password again",
            "min_length": "The password cannot be smaller than 6 characters. Please enter 6 to 14 characters",
            "max_length": "The password cannot be larger than 14 characters. Please enter 6 to 14 characters"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter the password again",
                "value": ""
            }
        )
    )

    captcha = CaptchaField(
        label="captcha",
        required=True,
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
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
            raise ValidationError("Username format entered wrong! Do not enter illegal characters")
        if not is_available_password(password):
            raise ValidationError("Password format entered wrong! Do not enter illegal characters")
        if not password == re_password:
            raise ValidationError("The two passwords are inconsistent!")
        if User.objects.filter(username=username).exists():
            raise ValidationError("The user already exists!")

        self.user = User.objects.create_user(username=username, password=password, identity=0, country=self.country)
        Profile.objects.create(user=self.user, profile="")
        return self.cleaned_data

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]


class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        min_length=6, max_length=14,
        label="old_password",
        error_messages={
            "required": "Please enter your password",
            "min_length": "The password cannot be smaller than 6 characters. Please enter 6 to 14 characters",
            "max_length": "The password cannot be larger than 14 characters. Please enter 6 to 14 characters"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Old password",
                "value": ""
            }
        )
    )

    password = forms.CharField(
        min_length=6, max_length=14,
        label="password",
        error_messages={
            "required": "Please enter your password",
            "min_length": "The password cannot be smaller than 6 characters. Please enter 6 to 14 characters",
            "max_length": "The password cannot be larger than 14 characters. Please enter 6 to 14 characters"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New password",
                "value": ""
            }
        )
    )

    re_password = forms.CharField(
        min_length=6, max_length=14,
        label="re-password",
        error_messages={
            "required": "Please enter your password again",
            "min_length": "The password cannot be smaller than 6 characters. Please enter 6 to 14 characters",
            "max_length": "The password cannot be larger than 14 characters. Please enter 6 to 14 characters"
        },
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter the new password again",
                "value": ""
            }
        )
    )

    captcha = CaptchaField(
        label="captcha",
        required=True,
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
        },
    )

    user: User

    def clean(self):
        super().clean()
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)
        old_password, password, re_password = \
            self.cleaned_data.get("old_password"), self.cleaned_data.get("password"), self.cleaned_data.get(
                "re_password")
        if (not is_available_password(old_password)) or (not self.user.check_password(old_password)):
            # check raw password
            raise ValidationError("Old password is incorrect!")
        if not is_available_password(password):
            raise ValidationError("Password format entered wrong! Do not enter illegal characters")
        if not password == re_password:
            raise ValidationError("The two new passwords are inconsistent!")
        if password == old_password:
            raise ValidationError("The old and new passwords are the same!")
        self.user.set_password(password)
        self.user.save()
        return self.cleaned_data

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]


class UserProfileForm(forms.Form):
    textarea = forms.CharField(
        min_length=1, max_length=200,
        label="textarea",
        error_messages={
            "required": "Please enter the profile",
            "min_length": "The profile cannot be smaller than 1 characters. Please enter 1 to 200 characters",
            "max_length": "The profile cannot be larger than 200 characters. Please enter 6 to 200 characters"
        },
        widget=forms.Textarea(
            attrs={
                "placeholder": "Say something...",
                "value": ""
            }
        )
    )
    captcha = CaptchaField(
        label="captcha",
        required=True,
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
        },
    )

    user: User

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]

    def clean(self):
        super().clean()
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)
        profile = self.cleaned_data.get("textarea").strip()
        if not is_available_profile(profile):
            raise ValidationError("Profile format entered wrong! Do not enter illegal characters")
        self.user.profile.profile = profile
        self.user.profile.save()
        print(self.user.profile.profile)
        return self.cleaned_data
