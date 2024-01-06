from django.urls import path, register_converter
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>', views.detail, name='article'),
    path('<int:article_id>/like', views.like, name='like'),
    path('<int:author_id>/author', views.author, name='author'),
]
