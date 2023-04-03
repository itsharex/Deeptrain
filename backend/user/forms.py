from django import forms
from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.functional import cached_property
from user.models import User
from utils.throttle import user_submit_detection, user_ip_detection
from django.utils.translation import gettext_lazy as _
from .fields import *

default_detail = "nothing..."


def is_available_profile(profile: str) -> bool:
    return 1 <= len(profile) <= 200


class AbstractForm(forms.Form):
    class Meta:
        abstract = True

    def get(self, key, default=None):
        return self.cleaned_data.get(key, default)

    @property
    def error(self):
        generator = iter(self.errors.get_json_data().values())
        errors = next(generator)
        return errors[0]['message']


class BaseUserForm(forms.Form):
    def __init__(self, request: WSGIRequest):
        super().__init__(data=request.POST or None, files=request.FILES or None)
        self.request = request

    def clean(self):
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)

    @cached_property
    def user(self) -> User:
        return self.request.user

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]

    def get_response(self) -> dict:
        if self.is_valid():
            return {"success": True}
        else:
            return {"success": False, "reason": self.get_error()}

    def as_response(self) -> JsonResponse:
        return JsonResponse(self.get_response())


class LoginForm(AbstractForm):
    username = UsernameField()
    password = PasswordField()
    captcha = TurnstileField()


class RegisterForm(AbstractForm):
    username = UsernameField()
    password = PasswordField()
    captcha = hCaptchaField()
    email = EmailField()


class ResetPasswordForm(BaseUserForm):
    password = PasswordField()
    captcha = TurnstileField()

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        self.user.set_password(password)
        self.user.save()
        auth.login(self.request, self.user)
        return self.cleaned_data


class UserProfileForm(BaseUserForm):
    profile = ProfileField()
    captcha = TurnstileField()

    def clean(self):
        super().clean()
        profile = self.cleaned_data.get("textarea").strip()
        if not is_available_profile(profile):
            raise ValidationError("Profile format entered wrong! Do not enter illegal characters")
        self.user.profile.profile = profile
        self.user.profile.save()
        return self.cleaned_data
