from django.contrib import admin
from .models import Tag, Article, Comment
from mptt.admin import MPTTModelAdmin

admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Comment, MPTTModelAdmin)
