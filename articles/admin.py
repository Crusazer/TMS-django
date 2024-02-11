from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.models import User

from .models import Article, Author

admin.site.empty_value_display = "(None)"


# Register your models here.
class AuthorInline(admin.TabularInline):
    model = Article.authors.through
    verbose_name = u"Author"
    verbose_name_plural = u"Authors"
    extra = 0


class ArticleInline(admin.TabularInline):
    model = Article.authors.through
    verbose_name = u"Article"
    verbose_name_plural = u"Articles"
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ['liked_users', 'is_popular', 'count_likes', 'authors']
    filter_horizontal = ('authors',)
    search_fields = ["title", "authors", "text"]
    list_display = ["title", 'is_popular']
    fieldsets = [
        (None, {'fields': ['title', 'authors']}),
        ('Content', {'fields': ['text']}),
        ('Likes information', {'fields': ['is_popular', 'count_likes', "liked_users"]})
    ]

    exclude = ("authors",)
    inlines = (AuthorInline,)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ["articles"]
    fieldsets = [
        (None, {'fields': ['first_name', "last_name", "date_of_birth"]}),
        ("Created articles", {"fields": ["articles"]})
    ]
    inlines = (ArticleInline,)
