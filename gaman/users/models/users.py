"""User models."""

# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Utils
from gaman.utils.models import GamanModel


class User(GamanModel, AbstractUser):
    """
    User model.
    Extend from Django's Abstract User and add some extra fields.
    """

    # Roles choices
    ROLES = [
        ('Athlete', 'Athlete'),
        ('Sponsor', 'Sponsor'),
        ('Coach', 'Coach'),
        ('League president', 'League president')
    ]

    email = models.EmailField(
        'email address', unique=True,
        error_messages={'unique': 'A user with that email already exists.'})

    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')

    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)

    verified = models.BooleanField(
        default=False, help_text='Set to true when the user have verified its email add')

    role = models.CharField(
        help_text='role of user.', max_length=16, choices=ROLES)

    # Username configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'role']

    def is_data_completed(self) -> bool:
        """Return the status of the user data."""
        if not self.phone_number:
            return False
        return True

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username