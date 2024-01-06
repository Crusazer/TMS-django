from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.models import User

from .models import Article, Author


# Register your models here.
class AuthorInline(admin.TabularInline):
    model = Article.authors.through
    verbose_name = u"Author"
    verbose_name_plural = u"Authors"


class ArticleInline(admin.TabularInline):
    model = Article.authors.through
    verbose_name = "Article"
    verbose_name_plural = "Articles"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ['users', 'is_popular', 'count_likes', 'authors']
    filter_horizontal = ('authors',)
    search_fields = ["title", "authors", "text"]
    list_display = ["title", 'is_popular']
    fieldsets = [
        (None, {'fields': ['title', 'authors']}),
        ('Content', {'fields': ['text']}),
        ('Likes information', {'fields': ['is_popular', 'count_likes', "users"]})
    ]

    exclude = ("authors",)
    inlines = (AuthorInline,)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    inlines = (ArticleInline,)
