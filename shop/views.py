from functools import reduce

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F, Sum, ExpressionWrapper, IntegerField
from django.http import HttpRequest
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Category, Product, OrderEntry, Order
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


class AddToCartView(LoginRequiredMixin, SingleObjectMixin, generic.View):
    model = Product
    pk_url_kwarg = "product_id"

    def get(self, request: HttpRequest, *args, **kwargs):
        product = self.get_object()
        shopping_cart = request.user.profile.shopping_cart
        shopping_cart.order_entries.update_or_create(product=product, defaults={'count': F("count") + 1},
                                                     create_defaults={"product": product, "order": shopping_cart})

        return redirect(request.GET.get("next", 'shop:products'))


class MyShoppingCart(LoginRequiredMixin, generic.View):
    model = OrderEntry
    context_object_name = "shopping_cart"
    template_name = "shop/shopping_cart.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        shopping_cart: Order = request.user.profile.shopping_cart

        context = {self.context_object_name: shopping_cart, "total": shopping_cart.total_price(),
                   "shopping_cart": shopping_cart.order_entries.all().order_by("id")}
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, *args, **kwargs):
        shopping_cart: Order = request.user.profile.shopping_cart

        match request.GET.get("method", False):
            # update count of order_entry
            case "update":
                count: int = int(request.POST.get('count', 1))
                order_entry_id = request.POST.get('id')
                order_entry: OrderEntry = shopping_cart.order_entries.get(pk=order_entry_id)
                order_entry.update(count)

            # delete order_entry from shopping cart
            case "delete":
                order_entry_id: int = int(request.POST.get('id'))
                order_entry: OrderEntry = shopping_cart.order_entries.get(pk=order_entry_id)
                order_entry.delete()

            # confirm order and clear chopping cart
            case "confirm":
                if shopping_cart.order_entries.exists():
                    profile = request.user.profile
                    shopping_cart.status = Order.Status.COMPLETED
                    profile.shopping_cart = Order.objects.create(status=Order.Status.INITIAL, profile=profile)

                    shopping_cart.save()
                    profile.save()

                    messages.success(request, "Order successfully placed")

            # clear all shopping cart
            case "clear":
                shopping_cart.order_entries.all().delete()

        return redirect(reverse("shop:shopping_cart"))


class UserProfile(LoginRequiredMixin, generic.View):
    model = User
    template_name = "shop/user_profile.html"
    pk_url_kwarg = "profile"

    def get(self, request: HttpRequest, *args, **kwargs):
        last_five_orders: list[Order] = request.user.profile.orders.filter(status=Order.Status.COMPLETED).order_by(
            '-id')[:5]
        return render(request, self.template_name, context={"last_five_orders": last_five_orders})

    def post(self, request: HttpRequest, *args, **kwargs):
        user: User = request.user

        match request.POST.get("action", None):
            # change username of user
            case "username":
                user.username = request.POST.get("username", user.username)

            # change firstname of user
            case "first_name":
                user.first_name = request.POST.get("first_name", user.first_name)

            case "last_name":
                user.last_name = request.POST.get("last_name", user.last_name)

            case "email":
                user.email = request.POST.get("email", user.email)

        user.save()
        return redirect(reverse('shop:user_profile'))


class OrderHistory(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "shop/order_history.html"
    context_object_name = "orders"
    paginate_by = 1

    def get_queryset(self):
        return self.request.user.profile.orders.filter(status=Order.Status.COMPLETED).order_by("id")

    def post(self, request: HttpRequest, *args, **kwargs):
        request.user: User
        shopping_cart: Order = request.user.profile.shopping_cart

        # load selected order
        order = get_object_or_404(Order, pk=request.POST.get("order_id", 0))

        # Clear current shopping cart
        shopping_cart.order_entries.all().delete()

        # load order_entries to shoppingcart from selected order
        OrderEntry.objects.bulk_create(
            OrderEntry(count=order_entry.count, product=order_entry.product, order=shopping_cart) for order_entry in
             order.order_entries.all())

        messages.success(request, "Order successfully placed into your shoppingcart")
        return redirect(reverse("shop:shopping_cart"))
