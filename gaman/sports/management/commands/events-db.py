"""Events command."""

# Utilities
import random
import pandas as pd

# Django
from django.core.management.base import BaseCommand

# Models
from gaman.sports.models import Club, SportEvent


class Command(BaseCommand):
    """League command"""

    help = 'Upload sport events csv to database'

    def handle(self, *args, **options):
        events_data = pd.DataFrame(
            pd.read_csv('./data/events.csv'),
            columns=['title', 'description', 'start', 'finish', 'country']
        )

        clubs = Club.objects.all()
        events_query = []
        limit = clubs.count() - 1
        for event_data in events_data.itertuples():
            event_query = SportEvent(
                club=clubs[random.randint(0, limit)],
                title=event_data.title,
                description=event_data.description,
                photo='gaman/utils/media_test/profile_photo.jpg',
                start=event_data.start,
                finish=event_data.finish,
                country=event_data.country
            )
            events_query.append(event_query)

        SportEvent.objects.bulk_create(events_query)

        self.stdout.write(self.style.SUCCESS('Sport events created successfully.'))
