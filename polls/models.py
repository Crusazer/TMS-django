from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Question(models.Model):
    class Status(models.TextChoices):
        NEW = 'NW', _('New')
        REJECTED = 'RJ', _('Rejected')
        APPROVED = 'AP', _('Approved')

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', db_index=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.NEW)
    objects: QuerySet = models.Manager()

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        description='Published recently?',
        ordering='pub_date'
    )
    def was_published_recently(self):
        if not self.pub_date:
            return False
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    objects: QuerySet

    def __str__(self):
        return f"{self.question.question_text} - {self.choice_text}"

    @admin.display(
        description="Question"
    )
    def get_question_text(self):
        return self.question.question_text

