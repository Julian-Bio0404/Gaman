"""Leagues commands."""

# Utilities
import pandas as pd

# Django
from django.core.management.base import BaseCommand

# Models
from gaman.sports.models import League
from gaman.users.models import User


class Command(BaseCommand):
    """League command"""

    help = 'Upload league csv to database'

    def handle(self, *args, **options):
        leagues_data = pd.DataFrame(
            pd.read_csv('./data/leagues.csv'),
            columns=['slugname', 'about', 'official_web']
        )

        users = User.objects.filter(role='League president', verified=True)
        countries = [user.profile.country for user in users]
        
        x, leagues_query = 0, []
        for league_data in leagues_data.itertuples():
            league_query = League(
                photo='gaman/utils/media_test/profile_photo.jpg',
                cover_photo='gaman/utils/media_test/profile_photo.jpg',
                about=league_data.about,
                slugname=league_data.slugname,
                country=countries[x],
                official_web=league_data.official_web,
                sport=users[x].profile.sport
            )
            leagues_query.append(league_query)
            x += 1

        League.objects.bulk_create(leagues_query)

        self.stdout.write(self.style.SUCCESS('Leagues created successfully.'))