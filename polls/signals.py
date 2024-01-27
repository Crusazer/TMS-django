import django
from django.db.models import signals
from django.dispatch import receiver

from polls.models import Question
from polls.models import Choice


# @receiver(django.db.models.signals.post_save, sender=Question)
# def post_saved_signal_from_question(sender, instance, created, **kwargs):
#     print(f"Question object saved. Sender: {sender}, Instance: {instance},\tCreated: {created}, \tkwargs: {kwargs}")
#
#
# @receiver(signals.post_delete, sender=Question)
# def post_delete_signal_from_question(sender, instance, **kwargs):
#     print(f"Question object deleted. Sender: {sender}, \tInstance: {instance}, \tkwargs: {kwargs}")
#
#
# @receiver(signals.post_init, sender=Question)
# def post_init_signal_from_question(sender, instance, **kwargs):
#     print(f"Question post init. sender: {sender}, \tinstance: {instance}")
#
#
# """---------------------------- CHOICES -------------------------------------------"""
#
#
# @receiver(django.db.models.signals.post_save, sender=Choice)
# def post_saved_signal_from_question(sender, instance, created, **kwargs):
#     print(f"Choice object saved. Sender: {sender}, Instance: {instance},\tCreated: {created}, \tkwargs: {kwargs}")
#
#
# @receiver(signals.post_delete, sender=Choice)
# def post_delete_signal_from_question(sender, instance, **kwargs):
#     print(f"Choice object deleted. Sender: {sender}, \tInstance: {instance}, \tkwargs: {kwargs}")
#
#
# @receiver(signals.post_init, sender=Choice)
# def post_init_signal_from_question(sender, instance, **kwargs):
#     print(f"Choice post init. sender: {sender}, \tinstance: {instance}")
