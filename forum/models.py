from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔐 Доступ только для зарегистрированных пользователей
    is_private = models.BooleanField(default=False)

    file = models.FileField(
        upload_to='posts/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    file = models.FileField(
        upload_to='comments/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Комментарий от {self.author.username}'