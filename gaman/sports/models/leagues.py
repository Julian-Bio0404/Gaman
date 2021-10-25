"""League model."""

# Django
from django.db import models

# Utils
from gaman.utils.models import BaseDataModel, GamanModel


class League(GamanModel, BaseDataModel):
    """League model."""

    photo = models.ImageField(
        help_text='league photo',
        upload_to='sports/leagues/photos%Y/%m/%d/', blank=True, null=True)

    cover_photo = models.ImageField(
        help_text='league cover photo',
        upload_to='sports/leagues/cover_photos/%Y/%m/%d/', blank=True, null=True)

    country = models.CharField(
        help_text='Country of the league', max_length=60, blank=True)

    state = models.CharField(
        help_text='State of the origin', max_length=60, blank=True)

    sport = models.CharField(
        help_text='sport of the origin', max_length=60, blank=True)

    def __str__(self):
        """Return League's slugname."""
        return self.slugname