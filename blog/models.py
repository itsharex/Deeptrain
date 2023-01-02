from django.db import models
from user.models import User
from mdeditor.fields import MDTextField


class Tag(models.Model):
    tag = models.SlugField(max_length=20, default="")

    def __str__(self):
        return f"Tag Object ({self.tag})"


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    title = models.CharField(max_length=50, default="")
    content = MDTextField(default="")
    preview = models.TextField(max_length=120, default="")
    published_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, related_name="like_users")

    def __str__(self):
        return f"{self.author.username}'s Article - {self.title}"
