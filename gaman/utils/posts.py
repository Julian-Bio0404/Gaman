"""Posts utils."""

# Utilities
import typing as t

# Models
from gaman.posts.models import Post
from gaman.sponsorships.models import Brand
from gaman.sports.models import Club
from gaman.users.models import User


class PostAuthorContext:
    """
    Create a Post according to the author context.
    """

    @classmethod
    def create_post(
        cls, data: dict, author: t.Union[User, Brand, Club]) -> Post:
        author_type = type(author)
        if author_type == User:
            data['user'] = author
        elif author_type == Brand:
            data['brand'] = author
        elif author_type == Club:
            data['club'] = author
        post = Post.objects.create(**data)
        return post
