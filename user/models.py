from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from utils.webtoken import generate_token
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

identities = {
    0: "User",
    1: "VIP",  # Very Important Person
    2: "Admin",
    3: "Server-Owner",
}

identity_choices = list(identities.items())


class User(AbstractUser):
    class Meta:
        db_table = "auth"
        verbose_name = "User"

    identity = models.SmallIntegerField(choices=identity_choices, default=0)
    country = models.TextField(max_length=50, default="Unknown")

    def __int__(self):
        return self.id

    @cached_property
    def is_admin(self) -> bool:
        return self.identity >= 2

    @cached_property
    def real_identity(self) -> str:
        return identities[self.identity]

    @cached_property
    def url(self) -> str:
        return f"/profile/?id={self.id}"

    def __str__(self):
        return f"{self.username} (identity: {self.real_identity}, id: {self.id})"

    @cached_property
    def token(self):
        return generate_token(self.username, self.password)

    @cached_property
    def simple_tag(self):
        return "admin" if self.is_admin else "user"

    @cached_property
    def text_profile(self):
        return self.profile.profile

    @cached_property
    def avatar_url(self) -> str:
        return self.profile.avatar.url


class Profile(models.Model):
    class Meta:
        db_table = "user_profile"
        verbose_name = "User Profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.TextField(default="", max_length=200)
    avatar = ProcessedImageField(
        upload_to='avatars',
        default='avatars/default.png',
        processors=[ResizeToFill(100, 100)]
    )

    github = models.CharField(max_length=25, default="")
    gitee = models.CharField(max_length=25, default="")

    def __str__(self):
        return f"Profile object ({self.user})"

    def __int__(self):
        return self.id
