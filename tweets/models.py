from django.conf import settings
from django.db import models


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="内容", max_length=140)
    created_at = models.DateTimeField(verbose_name="投稿日", auto_now_add=True)
