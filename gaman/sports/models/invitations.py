"""Invitation models."""

# Django
from django.db import models

# Utils
from gaman.utils.models import GamanModel


class Invitation(GamanModel):
    """Invitation model."""

    issued_by = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        help_text='Club coach that is providing the invitation')
    
    invited = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        help_text='Athlete that used the invitation to enter the club.',
        related_name='invited')
    
    club = models.ForeignKey('sports.Club', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def __str__(self):
        """Return club and athlete."""
        return f'{self.issued_by} from {self.club}: {self.invited}'