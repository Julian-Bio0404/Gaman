"""Event models."""

# Django
from django.db import models

# Utils
from gaman.utils.models import GamanModel


class SportEvent(GamanModel):
    """
    Sport Event model.
    This model stores sport events.
    It can be created by a user, sports club,
    a federation or a brand.
    """

    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey('sponsorships.Brand', on_delete=models.SET_NULL, null=True)
    club = models.ForeignKey('sports.Club', on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, blank=True)

    photo = models.ImageField(
        help_text='Event picture', upload_to='sports/events/pictures/%Y/%m/%d/', blank=True, null=True)
    
    start = models.DateField(
        help_text='sport event start date', auto_now=False, auto_now_add=False)

    finish = models.DateField(
        help_text='sport event finish date', auto_now=False, auto_now_add=False)
    
    geolocation = models.CharField(max_length=33)
    assistants = models.ManyToManyField('users.User', blank=True, related_name='assistants')

    def __str__(self):
        """Return Event title."""
        return self.title
