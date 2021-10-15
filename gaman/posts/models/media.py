"""Media models."""

# Django
from django.db import models

# Utilities
from gaman.utils.models import BaseGamanModel


class Picture(BaseGamanModel):
    """Picture model."""

    content = models.ImageField(
        help_text='Post picture', upload_to='posts/pictures/%Y/%m/%d/', blank=True, null=True)


class Video(BaseGamanModel):
    """Video model."""

    content = models.FileField(
        help_text='Post video', upload_to='posts/videos/%Y/%m/%d/', blank=True, null=True)