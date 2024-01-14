from django.contrib import admin
from .models import Product, Category


# Register your models here.
class ProductInline(admin.StackedInline):
    model = Product
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = (ProductInline,)