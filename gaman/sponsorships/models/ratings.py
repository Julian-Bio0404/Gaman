"""Rating models."""

# Django
from django.db import models

# Utils
from gaman.utils.models import BaseGamanModel


class Rating(BaseGamanModel):
    """Rating model."""

    sponsorship = models.ForeignKey(
        'sponsorships.Sponsorship', on_delete=models.SET_NULL, null=True)

    qualifier = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, blank=True)
    rating = models.DecimalField(max_digits=1, decimal_places=1)

    def __str__(self):
        """Return rating."""
        return f'{self.rating}'