from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
import controller


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
    captcha.widget.widgets[1].attrs.update({"placeholder": "验证码"})  # 似乎不管用

    def clean(self):
        super().clean()
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)
        username, password = self.cleaned_data.get("username"), self.cleaned_data.get("password")
        success, response = controller.login(username, password)
        if success:
            return self.cleaned_data
        else:
            raise ValidationError(response)

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
    captcha.widget.widgets[1].attrs.update({"placeholder": "验证码"})

    def clean(self):
        super().clean()
        captcha_error = self.errors.get("captcha")
        if captcha_error:
            raise ValidationError(captcha_error)
        username, password, re_password = \
            self.cleaned_data.get("username"), self.cleaned_data.get("password"), self.cleaned_data.get("re_password")
        success, response = controller.register(username, password, re_password)
        if success:
            return self.cleaned_data
        else:
            raise ValidationError(response)

    def get_error(self):
        return (self.errors.get("__all__") or self.errors.get("captcha"))[0]
