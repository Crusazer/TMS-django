from django.shortcuts import render, get_object_or_404

from shop.models import Category, Product


# Create your views here.
def index(request):
    context = {'categories': Category.objects.all().order_by('name')}
    return render(request, 'shop/index.html', context=context)


def detail(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'shop/detail.html', context=context)


def category(request, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    context = {'category': category}
    return render(request, 'shop/category.html', context=context)