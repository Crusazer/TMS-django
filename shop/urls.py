from django.urls import path, register_converter
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products', views.ProductsView.as_view(), name='products'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product'),
    path('category/<int:category_id>', views.CategoryDetailView.as_view(), name='category'),
    path('categories', views.CategoriesView.as_view(), name='categories')
]
