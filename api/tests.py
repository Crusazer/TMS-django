from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from articles.models import Article
from shop.models import Category, Product
from polls.models import Question, Choice


class TestMixin:
    path: str = None
    model = None
    related_model = None
    fields: list[str] = None
    answers: list[str] = None
    objects: list[model] = None
    related_objects: list[related_model] = None

    def test_empty_list(self):
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data, [])

    def test_list(self):
        if self.related_objects:
            self.related_model.objects.bulk_create(self.related_objects)

        self.model.objects.bulk_create(self.objects)
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(len(data), 2)
        self.assertEquals(data[0][self.fields[0]], self.answers[0])
        self.assertEquals(data[1][self.fields[0]], self.answers[1])

    def test_nonexistent_detail(self):
        response = self.client.get(f"{self.path}0/")
        self.assertEquals(response.status_code, 404)

    def test_detail(self):
        if self.related_objects:
            self.related_model.objects.bulk_create(self.related_objects)

        obj = self.objects[0]
        obj.save()
        response = self.client.get(f"{self.path}{obj.id}/")
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data[self.fields[0]], self.answers[0])


# Create your tests here.
class QuestionViewTest(TestCase, TestMixin):
    path = "/api/questions/"
    model = Question
    fields = ["question_text"]
    answers = ["Question1", "Question2"]
    objects = [model.objects.create(question_text=answers[0], pub_date=timezone.now()),
               model.objects.create(question_text=answers[1], pub_date=timezone.now())]


class ChoiceViewTest(TestCase, TestMixin):
    path = "/api/choices/"
    model = Choice
    related_model = Question
    fields = ["choice_text"]
    answers = ["Choice1", "Choice2"]
    related_objects = [Question.objects.create(question_text="Question", pub_date=timezone.now())]
    objects = [model.objects.create(question=related_objects[0], choice_text=answers[0]),
               model.objects.create(question=related_objects[0], choice_text=answers[1])]


class ArticleViewTest(TestCase, TestMixin):
    path = "/api/articles/"
    model = Article
    fields = ["title", "text"]
    answers = ["Title1", "Title2"]
    objects = [model.objects.create(title=answers[0], text="simple_text"),
               model.objects.create(title=answers[1], text="simple_text")]

    def test_post_create_object(self):
        data = {
            "choices": [],
            "question_text": "TEST QUESTION TEXT",
            "pub_date": "2022-01-01T00:00:00Z"
        }

        response = self.client.post(reverse("question-list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.filter(question_text='TEST QUESTION TEXT').count(), 1)


class CategoryViewTest(TestCase, TestMixin):
    path = "/api/categories/"
    model = Category
    fields = ["name"]
    answers = ["Cat1", "Cat2"]
    objects = [model.objects.create(name=answers[0]),
               model.objects.create(name=answers[1])]


class ProductViewTest(TestCase, TestMixin):
    path = "/api/products/"
    model = Product
    fields = ["name", "description", "price"]
    answers = ["Product1", "Product2"]
    related_model = Category
    related_objects = [Category.objects.create(name="cat")]
    objects = [model.objects.create(category=related_objects[0], name=answers[0], description="description", price=100),
               model.objects.create(category=related_objects[0], name=answers[1], description="description", price=100)]
