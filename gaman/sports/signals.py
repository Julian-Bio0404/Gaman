"""Sports signals."""

# Django
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Models
from gaman.sports.models import SportEvent

# Tasks
from taskapp.tasks.events import delete_sport_event


@receiver(pre_delete, sender=SportEvent)
def post_delete_event(sender, instance, *args, **kwargs):
    delete_sport_event.delay(pk=instance.pk, geolocation=instance.geolocation)
