from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product
from django.views import generic


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "shop/index.html"


class ProductsView(generic.ListView):
    paginate_by = 2
    model = Product
    context_object_name = "products"
    template_name = "shop/products.html"


class ProductDetailView(generic.DetailView):
    model = Product
    pk_url_kwarg = "product_id"
    context_object_name = "product"
    template_name = "shop/product.html"


class CategoryDetailView(generic.DetailView):
    model = Category
    pk_url_kwarg = "category_id"
    context_object_name = "category"
    template_name = "shop/category.html"


class CategoriesView(generic.ListView):
    model = Category
    context_object_name = "categories"
    template_name = "shop/categories.html"
