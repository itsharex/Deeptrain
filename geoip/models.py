from django.db import models
from model.models import User


class AdminIPHistory(models.Model):
    ip = models.GenericIPAddressField(default="127.0.0.1")
    country = models.CharField(max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class IPRequestAnalysis(models.Model):
    total = models.PositiveIntegerField(default=0)
    json_countries = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
