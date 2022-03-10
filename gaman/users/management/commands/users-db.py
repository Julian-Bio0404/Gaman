"""Users commands."""

# Utilities
import random
from django.db import IntegrityError
import pandas as pd

# Django
from django.core.management.base import BaseCommand

# Django REST Framework
from rest_framework.authtoken.models import Token

# Models
from gaman.users.models import FollowRequest, FollowUp, Profile, User


SPORTS = [
    'Athletics', 'Badminton', 'Basketball', 'Handball',
    'Baseball', 'Boxing', 'Cycling', 'Climbing', 'Fencing',
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
                'role', 'verified'
            ]
        )

        profiles_data = pd.DataFrame(
            pd.read_csv('./data/profiles.csv'),
            columns=[
                'about', 'birth_date', 'country',
                'public', 'web_site', 'social_link'
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
            ) for user_data in users_data.itertuples()
        ]

        users = User.objects.bulk_create(users_query)

        x, profiles_query = 0, []
        for profile_data in profiles_data.itertuples():
            profile_query = Profile(
                user=users[x],
                photo='gaman/utils/media_test/profile_photo.jpg',
                cover_photo='gaman/utils/media_test/profile_photo.jpg',
                about=profile_data.about,
                birth_date=profile_data.birth_date,
                country=profile_data.country,
                public=profile_data.public,
                web_site=profile_data.web_site,
                social_link=profile_data.social_link
            )
            profiles_query.append(profile_query)
            x += 1

        profiles = Profile.objects.bulk_create(profiles_query)
        for profile in profiles:
            if profile.user.role == 'Sponsor':
                continue
            profile.sport = random.choice(SPORTS)
        profiles = Profile.objects.bulk_update(profiles, ['sport'])


        for user in users:
            # Create follow requests
            requests_query = [
                FollowRequest(
                    follower=user,
                    followed=users[random.randint(0, 999)],
                    accepted=True
                ) for _ in range(10)
            ]
            requests = FollowRequest.objects.bulk_create(requests_query)

            # Create Follow-Up
            follow_query = [FollowUp(follower=user, user=i.followed) for i in requests]
            FollowUp.objects.bulk_create(follow_query)

        # Create User token
        verified_users = User.objects.filter(verified=True)
        for verified_user in verified_users:
            try:
                Token.objects.create(user=verified_user)
            except IntegrityError:
                pass

        self.stdout.write(
            self.style.SUCCESS('Users, Profiles, FollowUp and Follow-Requests created successfully.'))
