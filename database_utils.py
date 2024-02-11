import json
from django.utils import timezone

from articles.models import Author, Article
from polls.models import Question
from shop.models import Category, Product


def populate_polls_database(path: str, clean_database: bool = False):
    try:
        with open(path, 'r') as file:
            if clean_database:
                Question.objects.all().delete()

            data: dict = json.load(file)

            for question, choices in data.items():
                q = Question(question_text=f"{question}", pub_date=timezone.now())
                q.save()

                for choice, votes in choices.items():
                    q.choices.create(choice_text=f'{choice}', votes=votes)

    except FileNotFoundError:
        print(f'Файл {path} не был найден!')


def add_test_data_to_db():
    # ________________Shop data_______________________
    data = (
        ["Electronics", [("iPhone 12", "5G-enabled smartphone with A14 Bionic chip", 799),
                         ("Samsung Galaxy S21", "Android smartphone with triple camera system", 999),
                         ("Sony WH-1000XM4", "Wireless noise cancelling headphones", 349)]],
        ["Clothing",
         [("Levi's 501 Jeans", "Classic straight leg jeans", 59), ("Nike Air Force 1", "Iconic basketball shoes", 89),
          ("Lululemon Align Leggings", "High-waisted yoga pants", 98)]],
        ["Home Appliances", [("Instant Pot Duo", "7-in-1 multi-functional cooker", 79),
                             ("iRobot Roomba 675", "WiFi-connected robot vacuum", 249),
                             ("Ninja Foodi Pressure Cooker", "6.5-quart multi-cooker", 149)]],
        ["Beauty", [("Clinique Moisture Surge", "Hydrating facial moisturizer", 39),
                    ("Anastasia Beverly Hills Brow Wiz", "Fine-tipped brow pencil", 23),
                    ("Olaplex Hair Perfector No. 3", "Bond-building hair treatment", 28)]],
        ["Outdoor Gear", [("The North Face Thermoball Jacket", "Water-resistant insulated jacket", 199),
                          ("Yeti Hopper Flip 12", "Soft-sided cooler bag", 249),
                          ("Osprey Atmos AG 65 Backpack", "Lightweight hiking backpack", 270)]]
    )
    for i in data:
        # Create Categories
        category = Category.objects.create(name=i[0])
        # Create Products
        for product in i[1]:
            Product.objects.create(category=category, name=product[1], description=product[2],
                                   price=product[3])

    # __________________Article data__________________
    article_data = (
        ["Alice", "Smith"],
        [("The Impact of Climate Change on Biodiversity",
          "Climate change is a major threat to biodiversity as it leads to habitat loss and changes in ecosystems. This article discusses the various ways in which climate change affects different species and their survival."),
         ("Conservation Strategies for Endangered Species",
          "Endangered species are at risk of extinction, and conservation efforts play a crucial role in their protection. This article explores different strategies that can be used to conserve endangered species and their habitats."),
         ("The Importance of Genetic Diversity in Conservation",
          "Genetic diversity is essential for the long-term survival of species, as it provides resilience to changing environmental conditions. This article discusses the significance of genetic diversity in conservation efforts.")
         ],

        ["John", "Doe"],
        [("Sustainable Agriculture Practices for Food Security",
          "Sustainable agriculture practices are essential for ensuring food security for the growing global population. This article examines various sustainable farming methods that can help improve crop yields while preserving the environment."),
         ("The Role of Technology in Wildlife Conservation",
          "Technology plays a crucial role in wildlife conservation efforts, from tracking endangered species to monitoring habitats. This article explores the different ways in which technology is being used to protect wildlife and biodiversity.")
         ]

    )
    for i in article_data:
        author = Author.objects.create(first_name=i[0][0], last_name=i[0][1], date_of_birth=timezone.now())
        for article in i[1]:
            Article.objects.create(title=article[0], text=article[1], authors=author)

    # _________________Polls data________________
    polls_data = (
        "What is your favorite color?", ["Red", "Blue", "Green", "Yellow"],
        "What is your preferred mode of transportation?", ["Car", "Bus", "Train", "Bicycle"],
        "How often do you exercise?", ["Daily", "3-4 times a week", "1-2 times a week", "Rarely"],
        "What is your favorite type of cuisine?", ["Italian", "Mexican", "Chinese", "Indian"],
        "How do you prefer to relax?", ["Reading", "Watching TV", "Listening to music", "Exercising"],
    )

    for i in polls_data:
        q = Question.objects.create(question_text=i[0], pub_date=timezone.now(), status=Question.Status.APPROVED)
        for choice in i[1]:
            q.choices.create(choice_text=choice, votes=0)
