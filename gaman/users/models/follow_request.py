"""Follow Request models."""

# Django
from django.db import models

# Utils
from utils.models import BaseGamanModel


class FollowRequest(BaseGamanModel):
    """
    Follow Request model.
    For when the user wants to follow a private profile.
    """

    follower = models.ForeignKey('users.User', on_delete=models.CASCADE)

    followed = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='followed')
    
    accepted = models.BooleanField(default=False)

    def __str__(self):
        """Return follower and following."""
        return f'from @{self.follower} to @{self.followed}'