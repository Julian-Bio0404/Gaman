"""Users commands."""

# Utilities
import random
import pandas as pd

# Django
from django.core.management.base import BaseCommand

# Models
from gaman.users.models import FollowRequest, FollowUp, Profile, User


SPORTS = [
    'Athletics', 'Badminton', 'Basketball', 'Handball',
    'Baseball', 'Boxing', 'Cycling', 'Climbing', 'Fencing'
    'Soccer', 'Gymnastia', 'Golf', 'Halterophilia', 'Horse riding',
    'Hockey', 'Judo', 'Karate', 'Wrestling', 'Swimming',
    'Synchronized swimming', 'Pentathlon', 'Rowing', 'Rugby',
    'Jumping', 'Skateboarding', 'Surfing', 'Taekwondo',
    'Tennis', 'Table tennis', 'Shooting', 'Archery', 'Triathlon',
    'Sailing', 'Volleyball', 'Volleyball', 'Water polo'
]


class Command(BaseCommand):
    """User command."""

    help = 'Upload users and profiles csv to database'

    def handle(self, *args, **options):
        users_data = pd.DataFrame(
            pd.read_csv('./data/users.csv'),
            columns=[
                'first_name', 'last_name', 'username',
                'email', 'password', 'phone_number',
                'role', 'verified', 'created', 'updated'
    ]
        )

        profiles_data = pd.DataFrame(
            pd.read_csv('./data/profiles.csv'),
            columns=[
                'photo', 'cover_photo', 'about',
                'birth_date', 'country', 'public',
                'web_site', 'social_link'
            ]
        )

        users_query = [
            User(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                username=user_data.username,
                email=user_data.email,
                password=user_data.password,
                phone_number=user_data.phone_number,
                role=user_data.role,
                verified=bool(user_data.verified),
                created=user_data.created,
                updated=user_data.updated
            ) for user_data in users_data.itertuples()
        ]
        print(users_query)

        users = User.objects.bulk_create(users_query)

        profiles_query = [
            Profile(
                user=users[i],
                photo=profiles_data[i].photo,
                cover_photo=profiles_data[i].cover_photo,
                about=profiles_data[i].about,
                birth_date=profiles_data[i].birth_date,
                country=profiles_data[i].country,
                public=profiles_data[i].public,
                web_site=profiles_data[i].web_site,
                social_link=profiles_data[i].social_link
            ) for i in range(len(profiles_data))
        ]

        profiles = Profile.objects.bulk_create(profiles_query)
        for profile in profiles:
            if profile.user.role == 'Sponsor':
                continue
            profile.sport = random.choice(SPORTS)
        profiles = Profile.objects.bulk_update(profiles, ['sport'])

        # Create Follow Requests
        for user in users:
            requests_query = [
                FollowRequest(
                    follower=user,
                    followed=users[random.randint(0, 999)],
                    accepted=True
                ) for i in range(10)
            ]
            requests = FollowRequest.objects.bulk_create(requests_query)

            follow_query = [
                FollowUp(
                    follower=user,
                    user=i.followed
                ) for i in requests
            ]
            FollowUp.objects.bulk_create(follow_query)

        self.stdout.write(
            self.style.SUCCESS('Users, Profiles and Follow and Follow-Requests created successfully.'))
