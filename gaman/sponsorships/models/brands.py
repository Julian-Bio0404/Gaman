"""Brand models."""

# Django
from django.db import models

# Utils
from utils.models import GamanModel


class Brand(GamanModel):
    """Brand model."""

    slugname = models.SlugField(unique=True, max_length=40)

    photo = models.ImageField(
        help_text='brand photo', 
        upload_to='brands/photos/%Y/%m/%d/', blank=True, null=True) 

    cover_photo = models.ImageField(
        help_text='brand cover photo',
        upload_to='brands/cover_photos/%Y/%m/%d/', blank=True, null=True)

    about = models.TextField(
        help_text='write something about you', blank=True)

    official_web = models.URLField(
        help_text="brand's web site", max_length=200, blank=True)

    verified = models.BooleanField(default=False)

    def __str__(self):
        """Return brnad's slugname."""
        return self.slugname