import json
from django.utils import timezone

from polls.models import Question


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

