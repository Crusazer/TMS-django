from django.db import transaction

from django.utils import timezone

from .models import Question

from django.contrib.auth.models import User
from fake import FACTORY, DjangoModelFactory, pre_save, trait


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

    # Code below is too slow
    # @trait
    # def is_admin_user(self, instance: User) -> None:
    #     instance.is_superuser = True
    #     instance.is_staff = True
    #     instance.is_active = True
    #
    # @pre_save
    # def _set_password(self, instance: User) -> None:
    #     instance.set_password("test")


def create_question(question_text: str = '', days_diff=0, status=Question.Status.APPROVED):
    pub_data = timezone.now() + timezone.timedelta(days=days_diff)
    return Question.objects.create(question_text=question_text, pub_date=pub_data, status=status)


@transaction.atomic()
def transaction(raise_exception: bool = False):
    create_question(question_text='atomic1')
    if raise_exception:
        raise ValueError
    create_question(question_text='atomic2')
