"""SportEvents tasks."""

from __future__ import absolute_import, unicode_literals

# Utilities
import requests

# Django
from django.conf import settings

# Celery
from taskapp.celery import app

# Models
from gaman.sports.models import SportEvent


@app.task(bind=True)
def delete_sport_event(self, instance: SportEvent):
    """Delete sport event in geogaman service."""
    url = settings.GEOGAMAN_DOMAIN + 'zones/delete_events/'
    data = {
        'event_id': instance.pk,
        'geolocation': instance.geolocation
    }
    try:
        response = requests.post(url, data=data)
        return 'Success' if response.status_code == 200 else 'Unsuccess'
    except:
        return 'Unsuccess'
