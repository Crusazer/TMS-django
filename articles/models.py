from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, QuerySet
from django.utils import timezone


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_of_birth = models.DateTimeField(verbose_name="Day of birth", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField()

    liked_users = models.ManyToManyField(User, related_name="liked_articles", blank=True)
    authors = models.ManyToManyField(Author, related_name="articles", blank=False)
    objects: QuerySet

    def __str__(self):
        return self.title

    @admin.display(
        description='Is popular?',
        boolean=True,
    )
    def is_popular(self):
        return self.liked_users.count() > 100

    @admin.display(
        description="Count likes"
    )
    def count_likes(self):
        return self.liked_users.count()
