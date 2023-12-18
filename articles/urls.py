from django.urls import path, register_converter
from . import views

urlpatterns = [
    path('articles/', views.articles, name='articles'),
]
