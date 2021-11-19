"""Class utilities."""

# Models
from gaman.posts.models import Post
from gaman.users.models import User
from gaman.sponsorships.models import Brand
from gaman.sports.models import Club


class PostAuthorContext:
    """
    Create a Post according to the author context.
    """
    
    @classmethod
    def create_post(cls, data, author) -> Post:
        if type(author) == User:
            post = Post.objects.create(**data, user=author)
        elif type(author) == Brand:
            post = Post.objects.create(**data, brand=author)
        elif type(author) == Club:
            post = Post.objects.create(**data, club=author)
        return post