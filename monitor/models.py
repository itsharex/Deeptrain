from django.db import models


class RequestAnalysis(models.Model):
    class Meta:
        db_table = "monitor_request"
        verbose_name = "Request"

    date = models.DateField(auto_now_add=True, )
    request = models.PositiveIntegerField(default=0)
