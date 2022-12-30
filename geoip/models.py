from django.db import models


class IPRequestAnalysis(models.Model):
    class Meta:
        db_table = "geoip"
        verbose_name = "IP Analysis"

    total = models.PositiveIntegerField(default=0)
    json_countries = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
