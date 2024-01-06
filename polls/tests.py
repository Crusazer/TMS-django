from django.test import TestCase
from django.urls import reverse
from django.test import TestCase

from .models import Question
from .utilities_for_tests import UserFactory, create_question, transaction


# Create your tests here.
class QuestionModelTest(TestCase):
    def test_new_question_was_published_recently(self):
        self.assertTrue(create_question().was_published_recently())

    def test_old_question_was_not_published_recently(self):
        self.assertFalse(create_question(days_diff=-25).was_published_recently())

    def test_future_question_was_not_published_recently(self):
        self.assertFalse(create_question(days_diff=10).was_published_recently())


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')

    def test_future_question_and_past_question(self):
        past_question = create_question(question_text='past', days_diff=-30)
        create_question(question_text='future', days_diff=30)
        responce = self.client.get(reverse('polls:index'))
        self.assertEquals(responce.status_code, 200)
        self.assertQuerysetEqual(responce.context['latest_question_list'], [past_question])


class QuestionDetailViewTest(TestCase):
    def test_nonexistent_question(self):
        recponce = self.client.get(reverse('polls:detail', args=[0]))
        self.assertEquals(recponce.status_code, 404)

    def test_future_question(self):
        question = create_question(question_text='future', days_diff=20)
        recponce = self.client.get(reverse('polls:detail', args=[question.id]))
        self.assertEquals(recponce.status_code, 404)

    def test_past_question(self):
        question = create_question(question_text='past', days_diff=-10)
        recponce = self.client.get(reverse('polls:detail', args=[question.id]))
        self.assertEquals(recponce.status_code, 200)
        self.assertContains(recponce, question.question_text)

    def test_incorrect_transaction(self):
        self.assertRaises(ValueError, lambda: transaction(True))
        self.assertEquals(Question.objects.filter(question_text='atomic1').exists(), False)
        self.assertEquals(Question.objects.filter(question_text='atomic2').exists(), False)

        transaction(False)
        self.assertEquals(Question.objects.filter(question_text='atomic1').exists(), True)
        self.assertEquals(Question.objects.filter(question_text='atomic2').exists(), True)
