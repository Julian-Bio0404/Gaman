"""Brand models."""

# Django
from django.db import models

# Utils
from gaman.utils.models import BaseDataModel, GamanModel


class Brand(GamanModel, BaseDataModel):
    """Brand model."""

    sponsor = models.ForeignKey('users.User', on_delete=models.CASCADE)

    photo = models.ImageField(
        help_text='brand photo', 
        upload_to='brands/photos/%Y/%m/%d/', blank=True, null=True) 

    cover_photo = models.ImageField(
        help_text='brand cover photo',
        upload_to='brands/cover_photos/%Y/%m/%d/', blank=True, null=True)

    verified = models.BooleanField(default=False)

    def __str__(self):
        """Return Brand's slugname."""
        return self.slugname