from django import forms
from django.contrib import auth
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.functional import cached_property
from turnstile.fields import TurnstileField
from hcaptcha.fields import hCaptchaField
from django.core.exceptions import ValidationError
from user.models import User, Profile
from utils.throttle import user_submit_detection, user_ip_detection
from django.utils.translation import gettext_lazy as _

default_detail = "nothing..."


def isRegular(string: str) -> bool:
    return not any(map(lambda s: s in "\'\"<>~`?/\\*&^%$#@!:", string))


def is_available_username(username: str) -> bool:
    return 3 <= len(username) <= 12 and isRegular(username)


def is_available_password(password: str) -> bool:
    return 6 <= len(password) <= 14 and isRegular(password)


def is_available_profile(profile: str) -> bool:
    return 1 <= len(profile) <= 200


class AbstractForm(forms.Form):
    class Meta:
        abstract = True

    def get(self, key, default=None):
        return self.cleaned_data.get(key, default)


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
    username = forms.CharField(
        min_length=3, max_length=14, label="username",
        error_messages={
            "min_length": _("Length of username should be 3 to 14"),
            "max_length": _("Length of username should be 3 to 14"),
            "required": _("Please input username"),
        },
    )

    password = forms.CharField(
        min_length=6, max_length=26, label="password",
        error_messages={
            "required": _("Please input password"),
            "min_length": _("Length of password should be 6 to 26"),
            "max_length": _("Length of password should be 6 to 26"),
        },
    )

    captcha = TurnstileField(
        required=True, label="captcha",
        error_messages={
            "required": _("Please check the captcha"),
            "invalid": _("The captcha is incorrect"),
        },
    )

    def clean_username(self):
        if not isRegular((n := self.cleaned_data["username"])):
            raise ValidationError(_("The format of username is incorrect"))
        return n


class UserRegisterForm(BaseUserForm):
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

    captcha = hCaptchaField(
        label="captcha",
        required=True,
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
        },
    )

    def clean(self):
        super().clean()
        username, password, re_password = \
            self.cleaned_data.get("username"), self.cleaned_data.get("password"), self.cleaned_data.get("re_password")
        if not is_available_username(username):
            raise ValidationError("Username format entered wrong! Do not enter illegal characters")
        if not is_available_password(password):
            raise ValidationError("Password format entered wrong! Do not enter illegal characters")
        if not password == re_password:
            raise ValidationError("The two passwords are inconsistent!")
        user_submit_detection(self.request, "register")
        user_ip_detection(self.request)
        if User.objects.filter(username=username).exists():
            raise ValidationError("The user already exists!")

        user = User.objects.create_user(username=username, password=password, identity=0,
                                        country=getattr(self.request, "country"))
        Profile.objects.create(user=user, ip=getattr(self.request, "ip"))
        auth.login(self.request, user)
        return self.cleaned_data


class UserChangePasswordForm(BaseUserForm):
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

    captcha = TurnstileField(
        label="captcha",
        required=True,
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
        },
    )

    def clean(self):
        super().clean()
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
        auth.login(self.request, self.user)
        return self.cleaned_data


class UserProfileForm(BaseUserForm):
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
    captcha = TurnstileField(
        label="captcha",
        required=True,
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
        },
    )

    def clean(self):
        super().clean()
        profile = self.cleaned_data.get("textarea").strip()
        if not is_available_profile(profile):
            raise ValidationError("Profile format entered wrong! Do not enter illegal characters")
        self.user.profile.profile = profile
        self.user.profile.save()
        return self.cleaned_data
