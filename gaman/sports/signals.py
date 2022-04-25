"""Sports signals."""

# Django
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

# Models
from gaman.sports.models import SportEvent

# Tasks
from taskapp.tasks.events import create_sport_event, delete_sport_event


@receiver(post_save, sender=SportEvent)
def post_save_event(sender, instance, created, *args, **kwargs):
    if created:
        data = {
            'title': instance.title,
            'description': instance.description,
            'start': instance.start,
            'finish': instance.finish,
            'geolocation': instance.geolocation,
            'country': instance.country,
            'state': instance.state,
            'city': instance.city,
            'place': instance.place,
            'created': instance.created,
            'updated': instance.updated
        }
        create_sport_event.delay(data)


@receiver(pre_delete, sender=SportEvent)
def post_delete_event(sender, instance, *args, **kwargs):
    delete_sport_event.delay(instance.id)
