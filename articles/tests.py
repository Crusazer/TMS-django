from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Article

from fake import FACTORY, DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = FACTORY.username()
    first_name = FACTORY.first_name()
    last_name = FACTORY.last_name()
    email = FACTORY.email()
    last_login = FACTORY.date_time()
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()
    date_joined = FACTORY.date_time()

    class Meta:
        model = User
        get_or_create = ("username",)


def create_article(title: str = '', text: str = '') -> Article:
    return Article.objects.create(title=title, text=text)


# Create your tests here.
class ArticleIndexViewTest(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse("articles:index"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'There are no articles!')

    def test_contain_articles(self):
        article = create_article(title='Title', text='test')
        response = self.client.get(reverse("articles:index"))
        self.assertContains(response, article.title)


class DetailArticleViewTest(TestCase):
    def test_no_article_detail(self):
        response = self.client.get(reverse('articles:article', args=[0]))
        self.assertEquals(response.status_code, 404)

    def test_article_detail(self):
        article = create_article(title='Test title', text='Test text')
        response = self.client.get(reverse('articles:article', args=[article.pk]))
        self.assertContains(response, article.text)


class ModelArticleTest(TestCase):
    def test_is_popular(self):
        article = create_article(title='Popular test', )
        self.assertEquals(article.is_popular(), False)

        for user in UserFactory.create_batch(101):
            article.liked_users.add(user)

        self.assertEquals(article.is_popular(), True)
