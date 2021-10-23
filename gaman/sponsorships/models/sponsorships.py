"""Sponsorship models."""

# Django
from django.db import models

# Utils
from utils.models import GamanModel


class Sponsorship(GamanModel):
    """Sponsorship model."""

    sponsor = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='sponsor')
    
    athlete = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='athlete')

    club = models.ForeignKey('sports.Club', on_delete=models.SET_NULL, null=True)

    brand = models.ForeignKey(
        'sponsorships.Brand', on_delete=models.SET_NULL, null=True)

    start = models.DateField(
        help_text='sponsorship start date', auto_now=False, auto_now_add=False)

    finish = models.DateField(
        help_text='sponsorship finish date', auto_now=False, auto_now_add=False)

    active = models.BooleanField(default=False)

    def __str__(self):
        """Return Sponsorship's sponsor."""
        return f'{self.sponsor}'