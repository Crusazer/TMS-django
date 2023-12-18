from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField()
    category_id = models.ForeignKey(Category, related_name='category', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class UserToProduct(models.Model):
    user_id = models.ForeignKey(User, related_name='product_user', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id.name} : {self.product_id.name}'
