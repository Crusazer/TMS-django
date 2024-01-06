from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField()
    author = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="users", blank=True)

    def __str__(self):
        return self.title

    @admin.display(
        description='Is popular?',
        boolean=True,
    )
    def is_popular(self):
        return self.users.aggregate(count=Count('id'))['count'] > 100

    @admin.display(
        description="Count likes"
    )
    def count_likes(self):
        return self.users.aggregate(count=Count('id'))['count']
