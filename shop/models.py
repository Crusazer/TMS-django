from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet, Sum, F
from django.db.models.utils import AltersData
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField("Order", related_name="+", on_delete=models.SET_NULL, null=True, blank=True)
    objects: QuerySet
    orders: QuerySet

    def __str__(self):
        return f"Profile: {self.user.username}"


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


class Order(models.Model):
    class Status(models.TextChoices):
        INITIAL = "IN", _("Initial")
        COMPLETED = "CP", _("Completed")
        DELIVERED = "DL", _("Delivered")

    profile = models.ForeignKey(Profile, related_name="orders", on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=2, choices=Status, default=Status.INITIAL)
    objects: QuerySet
    order_entries: QuerySet

    def __str__(self):
        if self.status == "IN":
            return f"Shopping cart of {self.profile.user.username}"
        return f"Order of {self.profile.user.username} #{self.pk}"

    def total_price_db(self):
        return self.order_entries.filter(order=self).aggregate(
            total_price=Sum(F('product__price') * F('count')))[
            'total_price'] or 0

    def total_price(self):
        return sum(
            order_entries.product.price * order_entries.count for order_entries in self.order_entries.all()) or 0

    def total_count(self):
        return self.order_entries.all().aggregate(total_count=Sum('count'))['total_count'] or 0


class OrderEntry(models.Model):
    count = models.IntegerField(default=1, blank=False)
    product = models.ForeignKey(Product, related_name="order_entries", on_delete=models.CASCADE, blank=False)
    order = models.ForeignKey(Order, related_name="order_entries", on_delete=models.CASCADE, blank=False)
    objects: QuerySet

    def update(self, count: int):
        if count > 1:
            self.count = count
            self.save()
        else:
            self.delete()

    def __str__(self):
        return f"OrderEntry: {self.product}"
