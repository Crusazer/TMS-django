from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    objects: QuerySet

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0, blank=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, blank=False, null=True)
    objects: QuerySet

    def __str__(self):
        return self.name
