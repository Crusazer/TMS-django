from django.urls import path, register_converter
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:product_id>', views.detail, name='detail'),
    path('category/<int:category_id>', views.category, name='category'),
]