"""Member models."""

# Django
from django.db import models

# Utils
from gaman.utils.models import GamanModel


class Member(GamanModel):
    """
    Member model.
    A member is the table that holds the relationship
    between a user and a club.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        """Return username and club."""
        return f'@{self.user.username} at {self.club.slug_name}'
