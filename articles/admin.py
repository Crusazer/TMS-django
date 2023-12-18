from django.contrib import admin
from .models import Article, UserToArticle

# Register your models here.
admin.site.register(Article)
admin.site.register(UserToArticle)