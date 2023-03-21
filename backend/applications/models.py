from django.db import models
from user.models import User


class UserModel(models.Model):
    class Meta:
        abstract = True
    user = models.OneToOneField(User, on_delete=models.CASCADE)
