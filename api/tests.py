from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
import json

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

    def create_objects(self):
        """ Use to authomatic create objects in teste cases! """
        pass

    def create_relative_objects(self):
        """ Use if model has relative fields. """
        pass

    def multiple_create_objects(self, count: int):
        """ Used to create a specified number of objects """

    def test_empty_list(self):
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, 200)

        data = response.json()
        self.assertEquals(data["results"], [])

        self.create_objects()

        response = self.client.get(self.path)
        self.assertEquals(response.status_code, 200)

        data = response.json()
        if isinstance(data, dict):
            self.assertEquals(data["count"], 2)
            self.assertEquals(data["results"][0][self.fields[0]], self.answers[0])
            self.assertEquals(data["results"][1][self.fields[0]], self.answers[1])

    def test_nonexistent_detail(self):
        response = self.client.get(f"{self.path}0/")
        self.assertEquals(response.status_code, 404)

    def test_detail(self):
        if self.related_objects:
            self.related_model.objects.bulk_create(self.related_objects)

        self.create_objects()
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

    def create_objects(self):
        self.objects = [self.model.objects.create(question_text=self.answers[0], pub_date=timezone.now()),
                        self.model.objects.create(question_text=self.answers[1], pub_date=timezone.now())]

    def multiple_create_objects(self, count: int):
        answer = "Question"
        self.objects = [self.model.objects.create(question_text=answer + str(i), pub_date=timezone.now()) for i in
                        range(count)]

    def test_post_create_object(self):
        data = {
            "choices": [],
            "question_text": "TEST QUESTION TEXT",
            "pub_date": "2022-01-01T00:00:00Z"
        }

        response = self.client.post(reverse("question-list"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.filter(question_text='TEST QUESTION TEXT').count(), 1)

    def test_put_update_object(self):
        question = Question.objects.create(question_text="test", pub_date="1988-01-01T00:00:00Z")
        data = {
            "question_text": "New question text",
            "pub_date": timezone.now()
        }

        response = self.client.put(f"/api/questions/{question.id}/", data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "New question text")

    def test_delete_object(self):
        question = Question.objects.create(question_text="test", pub_date=timezone.now())
        response = self.client.delete(f"/api/questions/{question.id}/")
        self.assertEquals(response.status_code, 204)

        new_request = self.client.get("/api/questions/")
        self.assertEquals(new_request.json()['results'], [])

    def test_standard_search(self):
        self.multiple_create_objects(5)
        search_text = "Question2"
        response = self.client.get(f"/api/questions/?search={search_text}")

        self.assertEquals(response.status_code, 200)
        data = response.json()

        self.assertEquals(data['count'], 1)
        self.assertEquals(data['results'][0]["question_text"], search_text)

    def test_standard_order(self):
        self.create_objects()
        ordering = '-id'

        response = self.client.get(f"/api/questions/?ordering={ordering}")
        data = response.json()

        self.assertEquals(response.status_code, 200)
        self.assertTrue(data["results"][0]["id"] > data["results"][1]["id"])

    def test_pagination(self):
        """ Pagination used in all the tests and already checked """
        pass


class ChoiceViewTest(TestCase, TestMixin):
    path = "/api/choices/"
    model = Choice
    related_model = Question
    fields = ["choice_text"]
    answers = ["Choice1", "Choice2"]

    def create_objects(self):
        self.create_relative_objects()
        self.objects = [self.model.objects.create(question=self.related_objects[0], choice_text=self.answers[0]),
                        self.model.objects.create(question=self.related_objects[0], choice_text=self.answers[1])]

    def create_relative_objects(self):
        self.related_objects = [Question.objects.create(question_text="Question", pub_date=timezone.now())]

    def test_searching_of_choice_on_question(self):
        question1 = Question.objects.create(question_text="Question1", pub_date=timezone.now())
        self.model.objects.create(question=question1, choice_text="choice1"),
        self.model.objects.create(question=question1, choice_text="choice2")

        question2 = Question.objects.create(question_text="Question2", pub_date=timezone.now())
        self.model.objects.create(question=question2, choice_text="choice3"),

        searching_text = "question2"
        response = self.client.get(f"/api/choices/?search={searching_text}")
        self.assertEquals(response.status_code, 200)
        data = response.json()['results']

        self.assertEquals(data[0]["choice_text"], "choice3")


class ArticleViewTest(TestCase, TestMixin):
    path = "/api/articles/"
    model = Article
    fields = ["title", "text"]
    answers = ["Title1", "Title2"]

    def create_objects(self):
        self.objects = [self.model.objects.create(title=self.answers[0], text="simple_text"),
                        self.model.objects.create(title=self.answers[1], text="simple_text")]


class CategoryViewTest(TestCase, TestMixin):
    path = "/api/categories/"
    model = Category
    fields = ["name"]
    answers = ["Cat1", "Cat2"]
    objects = []

    def create_objects(self):
        self.objects = [self.model.objects.create(name=self.answers[0]),
                        self.model.objects.create(name=self.answers[1])]


class ProductViewTest(TestCase, TestMixin):
    path = "/api/products/"
    model = Product
    fields = ["name", "description", "price"]
    answers = ["Product1", "Product2"]
    related_model = Category

    def create_relative_objects(self):
        self.related_objects = [self.related_model.objects.create(name="cat")]

    def create_objects(self):
        self.create_relative_objects()
        self.objects = [
            self.model.objects.create(category=self.related_objects[0], name=self.answers[0], description="description",
                                      price=100),
            self.model.objects.create(category=self.related_objects[0], name=self.answers[1], description="description",
                                      price=100)]
