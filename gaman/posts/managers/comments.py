"""Comment managers."""

# Django
from django.db import models


class PrincipalCommentManager(models.Manager):
    """Principal Comment manager."""

    def get_queryset(self):
        """Filter the query to Principal Comments."""
        return super().get_queryset().filter(type='Principal-Comment')


class ReplyManager(models.Manager):
    """Reply manager."""

    def get_queryset(self):
        """Filter the query to replies."""
        return super().get_queryset().filter(type='Reply')