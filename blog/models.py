from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from user.models import User
from mdeditor.fields import MDTextField
from mptt.models import MPTTModel, TreeForeignKey
from utils.markdown_ import parse as parse_markdown


class Tag(models.Model):
    tag = models.SlugField(max_length=20, default="")

    def __str__(self):
        return f"Tag Object ({self.tag})"


class Article(models.Model):
    class Meta:
        ordering = ["-published_at"]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    title = models.CharField(max_length=50, default="")
    content = MDTextField(default="")
    preview = models.TextField(max_length=120, default="")
    published_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, related_name="like_users", blank=True)

    def __str__(self):
        return f"{self.author.username}'s Article - {self.title}"

    @property
    def likes_number(self) -> int:
        return self.likes.count()

    @cached_property
    def url(self):
        return reverse("blog:article", args=(self.id, ))

    def content_html(self):
        return parse_markdown(self.content)

    @cached_property
    def datetime(self):
        return self.published_at.strftime("%Y-%m-%d %H:%M:%S")

    @cached_property
    def date(self):
        return self.published_at.strftime("%Y-%m-%d")


class Comment(MPTTModel):
    class MPTTMeta:
        order_insertion_by = ['-created']

    content = models.TextField(max_length=300, default="")
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments", default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyer',
    )

    def __str__(self):
        return f"Comment Object of {self.article} (by: {self.user.username})"
