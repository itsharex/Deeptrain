import uuid
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from user.models import User
from DjangoWebsite.settings import MAX_FILE_NAME_LENGTH


class UserFile(models.Model):
    class Meta:
        verbose_name = "File"
        db_table = "file"

    id: models.AutoField
    real_name = models.CharField(max_length=MAX_FILE_NAME_LENGTH, default="")
    uuid_name = models.UUIDField(default=uuid.UUID('e306d9a1-1ba6-4a91-9005-7bd9296607fb'))
    size = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField

    objects: models.manager.Manager

    @cached_property
    def url(self):
        return reverse("files:download", kwargs={"uid": self.user.id, "ufile": self.uuid_name})

    @cached_property
    def json(self) -> dict:
        return {
            "id": self.user.id,
            "name": self.real_name,
            "time": self.time,
            "user": self.user.username,
            "size": self.size,
            "tag": self.user.simple_tag,
            "url": self.url,
        }
