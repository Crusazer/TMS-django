from django.contrib import admin
from .models import Question, Choice

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ["question_text", "pub_date"]
#     readonly_fields = ["pub_date"]
