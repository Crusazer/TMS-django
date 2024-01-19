import django
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver

from shop.models import Profile, Order


@receiver(django.db.models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)
        instance.profile.save()


@receiver(django.db.models.signals.post_save, sender=Profile)
def create_shopping_cart(sender, instance: Profile, created, **kwargs):
    if created:
        instance.shopping_cart = Order.objects.create(status=Order.Status.INITIAL, profile=instance)
        instance.save()