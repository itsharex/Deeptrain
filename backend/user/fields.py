from django.utils.translation import gettext_lazy as _
from django.forms import CharField, ValidationError
from django.core.validators import EmailValidator as _EmailValidator
from django.forms import EmailField as _EmailField
from turnstile.fields import TurnstileField as _TurnstileField
from hcaptcha.fields import hCaptchaField as _hCaptchaField


def invalid_text(string: str) -> bool:
    return any(map(lambda s: s in "\'\"<>~`?/\\*&^%$#@!:", string))


class UsernameField(CharField):
    def __init__(self, **kwargs):
        super().__init__(
            required=True, min_length=3, max_length=14, label="username",
            error_messages={
                "min_length": _("Length of username should be 3 to 14"),
                "max_length": _("Length of username should be 3 to 14"),
                "required": _("Please input username"),
                "invalid": _("Format of username is invalid"),
            }, **kwargs,
        )

    def validate(self, value):
        super().validate(value)
        if invalid_text(value):
            raise ValidationError(self.error_messages["invalid"], code="invalid")


class PasswordField(CharField):
    def __init__(self, **kwargs):
        super().__init__(
            required=True, min_length=6, max_length=26, label="password",
            error_messages={
                "required": _("Please input password"),
                "min_length": _("Length of password should be 6 to 26"),
                "max_length": _("Length of password should be 6 to 26"),
                "invalid": _("Format of username is invalid"),
            }, **kwargs,
        )

    def validate(self, value):
        super().validate(value)
        if invalid_text(value):
            raise ValidationError(self.error_messages["invalid"], code="invalid")


class EmailValidator(_EmailValidator):
    message = _("Format of email is invalid")
    domain_allowlist = [
        "gmail.com",
        "yahoo.com",
        "163.com",
        "qq.com",
        "dingtalk.com",
        "deeptrain.net",
    ]


class EmailField(_EmailField):
    def __init__(self, **kwargs):
        super().__init__(
            validators=(EmailValidator, ),
            required=True, label="email", **kwargs,
        )


class TurnstileField(_TurnstileField):
    def __init__(self, **kwargs):
        super().__init__(required=True, label="captcha", **kwargs)


class hCaptchaField(_hCaptchaField):
    def __init__(self, **kwargs):
        super().__init__(required=True, label="captcha", **kwargs)


class ProfileField(CharField):
    def __init__(self, **kwargs):
        super().__init__(
            required=True, max_length=200, label="profile",
            error_messages={
                "required": _("Please input profile"),
                "max_length": _("Length of profile should be 1 to 200"),
            }, **kwargs,
        )
