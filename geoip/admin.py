from django.contrib import admin
from .models import AdminIPHistory, IPRequestAnalysis

admin.site.register(AdminIPHistory)
admin.site.register(IPRequestAnalysis)
