from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class UserToArticle(models.Model):
    user_id = models.ForeignKey(User, related_name='article_user', on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, related_name='article', on_delete=models.CASCADE)

    def __str__(self):
        return f"Like: {self.user_id.name} to {self.article_id.name}"

