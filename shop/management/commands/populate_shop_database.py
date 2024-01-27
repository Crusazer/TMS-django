import json

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shop.models import Category, Product


class Command(BaseCommand):
    help = "Filling the file database with json file."

    def add_arguments(self, parser):
        parser.add_argument("--data_file_path", type=str, required=False, default="shop/management/commands/data.json")

    def handle(self, *args, **options):
        with open(options['data_file_path']) as file:
            data: dict = json.load(file)

            # Create categories
            Category.objects.bulk_create(Category(name=name) for name in data.get("Categories", ()))

            # Create products
            Product.objects.bulk_create(
                Product(name=product_data[0], description=product_data[1], price=product_data[2],
                        category=Category.objects.get(name=product_data[3])) for
                product_data in data.get('Products', ()))

            # Create users
            for user_data in data.get("Users", ()):
                User.objects.create_user(username=user_data[0], password=user_data[1])
