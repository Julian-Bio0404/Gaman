"""Clubs commands."""

# Utilities
import random
import pandas as pd

# Django
from django.core.management.base import BaseCommand

# Models
from gaman.sports.models import Club, League
from gaman.users.models import User


class Command(BaseCommand):
    """League command"""

    help = 'Upload league csv to database'

    def handle(self, *args, **options):
        clubs_data = pd.DataFrame(
            pd.read_csv('./data/clubs.csv'),
            columns=['slugname', 'about', 'official_web']
        )

        users = User.objects.filter(role='Coach', verified=True)
        leagues = League.objects.all()
        
        x, clubs_query = 0, []
        for club_data in clubs_data.itertuples():
            club_query = Club(
                trainer=users[x],
                league=leagues[random.randint(0, leagues.count()-1)],
                photo='gaman/utils/media_test/profile_photo.jpg',
                cover_photo='gaman/utils/media_test/profile_photo.jpg',
                about=club_data.about,
                slugname=club_data.slugname,
                official_web=club_data.official_web,
            )
            clubs_query.append(club_query)
            x += 1

        Club.objects.bulk_create(clubs_query)

        self.stdout.write(self.style.SUCCESS('Clubs created successfully.'))
