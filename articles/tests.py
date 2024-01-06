from django.test import TestCase
from django.urls import reverse
from .models import Article


def create_article(title: str = '', text: str = '', author: str = '') -> Article:
    return Article.objects.create(title=title, text=text, author=author)


# Create your tests here.
class ArticleIndexViewTest(TestCase):
    def test_no_articles(self):
        response = self.client.get(reverse("articles:index"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'There are no articles!')

    def rest_contain_articles(self):
        article = create_article(title='Title', text='test', author='no name')
        response = self.client.get(reverse("articles:index"))
        self.assertContains(response, article.title)


class DetailArticleViewTest(TestCase):
    def test_no_article_detail(self):
        response = self.client.get(reverse('articles:article', args=[0]))
        self.assertEquals(response.status_code, 404)

    def test_article_detail(self):
        article = create_article(title='Test title', text='Test text', author='Test name')
        response = self.client.get(reverse('articles:article', args=[article.pk]))
        self.assertContains(response, article.text)
