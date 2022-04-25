"""SportEvents tasks."""

from __future__ import absolute_import, unicode_literals

# Utilities
import requests

# Django
from django.conf import settings

# Celery
from taskapp.celery import app


@app.task(bind=True)
def create_sport_event(self, data: dict):
    """Send sport event to geogaman service."""
    url = settings.GEOGAMAN_DOMAIN + 'events/'
    try:
        response = requests.post(url, data=data)
        return 'Success' if response.status_code == 201 else 'Unsuccess'
    except:
        return 'Unsuccess'


@app.task(bind=True)
def update_sport_event(self, data: dict, event_id: int):
    """Send update of sport event to geogaman service."""
    url = settings.GEOGAMAN_DOMAIN + 'events/' + str(event_id)
    try:
        response = requests.patch(url, data=data)
        return 'Success' if response.status_code == 200 else 'Unsuccess'
    except:
        return 'Unsuccess'


@app.task(bind=True)
def delete_sport_event(self, event_id: int):
    """Send delete sport event to geogaman service."""
    url = settings.GEOGAMAN_DOMAIN + 'events/' + str(event_id)
    try:
        response = requests.delete(url)
        return 'Success' if response.status_code == 204 else 'Unsuccess'
    except:
        return 'Unsuccess'
