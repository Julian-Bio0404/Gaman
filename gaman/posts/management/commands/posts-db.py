"""Posts commands."""

# Utilities
import pandas as pd

# Django
from django.core.management.base import BaseCommand

# Models
from gaman.posts.models import Picture, Post
from gaman.users.models import User


class Command(BaseCommand):
    """Post command"""

    help = 'Upload posts and comment csv to database'

    def handle(self, *args, **options):
        posts_data = pd.DataFrame(
            pd.read_csv('./data/posts.csv'),
            columns=['about', 'privacy', 'location']
        )

        users = User.objects.filter(verified=True)
        posts_data = [data for data in posts_data.itertuples()]
        picture = Picture.objects.create(content='gaman/utils/media_test/profile_photo.jpg')
        
        posts_query = []
        x = 0
        for user in users:
            parcial_posts_data = posts_data[x:x+5]
            # Create posts
            parcial_posts_query = [
                Post(
                    user=user,
                    about=i.about,
                    location=i.location,
                    privacy='Private' if bool(i.privacy) == True else 'Public'
                ) for i in parcial_posts_data]
            x += 5
            posts_query += parcial_posts_query

        posts = Post.objects.bulk_create(posts_query)

        # Add picture to the posts
        for post in posts:
            post.pictures.add(picture)
            post.save()

        self.stdout.write(self.style.SUCCESS('Posts created successfully.'))
