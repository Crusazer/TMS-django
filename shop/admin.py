from django.contrib import admin
from .models import Product, UserToProduct, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(UserToProduct)
admin.site.register(Category)
