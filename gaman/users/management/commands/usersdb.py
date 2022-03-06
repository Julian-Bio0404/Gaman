"""Users commands."""

# Utilities
from datetime import datetime, timedelta
import pandas as pd

# Django
from django.core.management.base import BaseCommand

# Models
from gaman.users.models import FollowRequest, FollowUp, Profile, User


class Command(BaseCommand):
    """User command."""

    help = 'Upload users csv to database'

    def handle(self, *args, **options):
        users_data = pd.DataFrame(
            pd.read_csv('./data/users.csv'),
            columns=[
                'First_name', 'Last_name', 'Username',
                'Email', 'Password', 'Phone_number',
                'Phone_number', 'Role', 'Verified',
                'Created', 'Updated'
            ]
        )

        profile_data = pd.DataFrame(
            pd.read_csv('./data/profiles.csv'),
            columns=[
                'Photo', 'Cover_photo', 'About',
                'Birth_date', 'Country', 'Public',
                'Web_site', 'Social_link'
            ]
        )
        