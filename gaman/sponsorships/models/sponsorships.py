"""Sponsorship models."""

# Django
from django.db import models
from django.db.models.fields.related import ForeignKey

# Utils
from utils.models import GamanModel


class Sponsorship(GamanModel):
    """Sponsorship model."""

    sponsor = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    
    athlete = models,ForeignKey('users.User', on_delete=models.CASCADE)
    club = models.ForeignKey('sports.Club', on_delete=models.SET_NULL, null=True)

    brand = models.ForeignKey(
        'sponsorships.Brand', on_delete=models.SET_NULL, null=True)

    start = models.DateField(
        help_text='sponsorship start date', auto_now=False, auto_now_add=False)

    finish = models.DateField(
        help_text='sponsorship finish date', auto_now=False, auto_now_add=False)

    active = models.BooleanField(default=False)

    def __str__(self):
        """Return user's username."""
        return f'{self.sponsor}'