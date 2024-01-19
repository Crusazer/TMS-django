from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Product, Category, Order, OrderEntry, Profile


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


class OrderEntryInline(admin.StackedInline):
    model = OrderEntry
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderEntryInline]


@admin.register(OrderEntry)
class OrderEntryAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
