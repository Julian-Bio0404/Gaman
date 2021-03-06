"""Celery app config."""

from __future__ import absolute_import, unicode_literals

# Utilities
import os

# Celery
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('taskapp', include=['taskapp.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
