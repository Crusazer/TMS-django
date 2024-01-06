from django.contrib import admin
from .models import Article


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ['users', 'is_popular', 'count_likes']
    fieldsets = [
        (None, {'fields': ['title', 'author']}),
        ('Likes information', {'fields': ['is_popular', 'count_likes', "users"]})
    ]
    list_display = ["title", "author", 'is_popular']
