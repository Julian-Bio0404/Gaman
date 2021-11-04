"""Sponsorship models."""

# Django
from django.db import models

# Utils
from gaman.utils.models import GamanModel


class Sponsorship(GamanModel):
    """
    Sponsorship model.

    The fields that are SET_NULL, are for: 

        - sponsor: for not lose the info of the
        sponosorships in case the sponsor is deleted.

        - brand: it is optional, in case the sponsor
        does not has a brand.

        - athlete and club for allow to sponsor
        create a instance with two options: athlete or club.
    """

    sponsor = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='sponsor')
    
    athlete = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='athlete')

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