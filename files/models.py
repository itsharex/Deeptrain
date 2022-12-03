import os
import uuid
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from model.models import User
from DjangoWebsite.settings import FILE_DATABASE_DIR, MAX_FILE_NAME_LENGTH, MAX_FILE_SIZE
from controller import get_profile_from_user

registered_files = []

TOTAL_FILES = 0


def register_file(app, path):
    global registered_files
    registered_files.append((app, path))


def get_directory(uid, ufile):
    return os.path.join(FILE_DATABASE_DIR, str(uid), ufile)


def mix_directory(user, ufile):
    parent = os.path.join(FILE_DATABASE_DIR, str(user.id))
    if not os.path.exists(parent):
        os.mkdir(parent)
    return os.path.join(parent, ufile)


def get_file_url(user: User, ufile):
    return reverse("files:download", kwargs={"uid": user.id, "ufile": ufile})


def save_file(user: User, file: File):
    if file is None:
        raise ValidationError("File is none.")
    real_filename = file.name
    if len(file.name) > MAX_FILE_NAME_LENGTH:
        raise ValidationError("File name is too long.")
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("File is to large.")
    uuid_filename = str(uuid.uuid5(uuid.NAMESPACE_DNS, real_filename))
    path = mix_directory(user, uuid_filename)
    if os.path.exists(path):
        raise ValidationError("File is already exists.")
    with open(path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    UserFile.objects.create(real_name=real_filename, uuid_name=uuid_filename, user_bind=user, size=file.size)
    return get_file_url(user, uuid_filename)


class UserFile(models.Model):
    id: models.AutoField
    real_name = models.CharField(max_length=MAX_FILE_NAME_LENGTH, default="")
    uuid_name = models.UUIDField(default=uuid.uuid4())
    size = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    user_bind = models.ForeignKey(User, on_delete=models.CASCADE)

    objects: models.manager.Manager

    @cached_property
    def to_jsonable(self) -> dict:
        return {
            "id": self.user_bind.id,
            "name": self.real_name,
            "time": self.time,
            "user": self.user_bind.username,
            "size": self.size,
            "tag": "admin" if get_profile_from_user(self.user_bind).is_admin() else "user",
            "url": get_file_url(self.user_bind, self.uuid_name),
        }
