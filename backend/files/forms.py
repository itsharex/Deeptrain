import os
import uuid
from django import forms
from django.core.exceptions import ValidationError
from turnstile.fields import TurnstileField as CaptchaField
from user.forms import BaseUserForm
from .models import UserFile
from Deeptrain.settings import FILE_DATABASE_DIR, MAX_FILE_NAME_LENGTH, MAX_FILE_SIZE


def get_directory(uid, ufile):
    return os.path.join(FILE_DATABASE_DIR, str(uid), ufile)


def mix_directory(user, ufile):
    parent = os.path.join(FILE_DATABASE_DIR, str(user.id))
    if not os.path.exists(parent):
        os.mkdir(parent)
    return os.path.join(parent, ufile)


class FileForm(BaseUserForm):
    file = forms.FileField(
        label="file",
        allow_empty_file=False,
        required=True,
        max_length=MAX_FILE_NAME_LENGTH,
        error_messages={
            "max_length": f"The file name cannot be larger than {MAX_FILE_NAME_LENGTH} characters.",
            "required": "Please enter the file",
        },
        widget=forms.FileInput(
            attrs={
                "class": "hidden",
            }
        ),
    )

    captcha = CaptchaField(
        theme="dark",
        error_messages={
            "required": "Please enter the captcha field",
            "invalid": "The captcha is incorrect"
        },
    )

    url: str

    def clean(self):
        super().clean()
        file = self.cleaned_data.get("file")
        if not file:
            raise ValidationError("File is empty!")
        uuid_filename = str(uuid.uuid5(uuid.NAMESPACE_DNS, file.name))
        path = mix_directory(self.user, uuid_filename)
        if os.path.exists(path):
            raise ValidationError("File is already exists.")
        with open(path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        self.url = \
            UserFile.objects.create(real_name=file.name, uuid_name=uuid_filename, user=self.user, size=file.size).url
        return self.cleaned_data

    def get_response(self) -> dict:
        if self.is_valid():
            return {"success": True, "link": self.url}
        else:
            return {"success": False, "error": self.get_error()}
