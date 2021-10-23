"""Club models."""

# Django
from django.db import models

# Utils
from utils.models import BaseDataModel, GamanModel


class Club(GamanModel, BaseDataModel):
    """Club model."""

    league = models.ForeignKey('sports.League', on_delete=models.SET_NULL, null=True)

    photo = models.ImageField(
        help_text='Club photo',
        upload_to='sports/clubs/photos%Y/%m/%d/', blank=True, null=True)

    cover_photo = models.ImageField(
        help_text='Club cover photo',
        upload_to='sports/clubs/cover_photos/%Y/%m/%d/', blank=True, null=True)
    
    city = models.CharField(
        help_text='State of the origin', max_length=60, blank=True)
    
    trainer = models.ForeignKey('users.User', on_delete=models.CASCADE)

    members = models.ManyToManyField(
        'users.User', through='sports.Member',
        through_fields=('club', 'user'), related_name='members')

    def __str__(self):
        """Return Club's slugname."""
        return self.slugname