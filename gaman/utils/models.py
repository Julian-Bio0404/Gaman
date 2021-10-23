"""Django models utilities."""

# Django
from django.db import models


class BaseGamanModel(models.Model):
    """
    Base Gaman Model.

    BaseGamanModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following atribute:
        + created (DateTime): Store the datetime the object was created.
    """

    created = models.DateTimeField(
        'created at', auto_now_add=True,
        help_text='Date time on which the was created.')

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created']


class GamanModel(BaseGamanModel):
    """
    Gaman Model.

    GamanModel acts as an abstract base class inherits from
    BaseGamanModel. Extend your models of this class to add 
    the following field:
        + updated (DateTime): Store the datetime the object was updated.
    """

    updated = models.DateTimeField(
        'updated at', auto_now=True,
        help_text='Date time on which the was updated.')

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-updated']


class Reaction(BaseGamanModel):
    """
    Reaction model.
    
    Reaction acts as an abstract class inherits from
    BaseGamanModel. Extend your models of this class
    to add the following field:
        + reaction (Charfield): Store the type reaction to object.
    """

    # Reaction choices
    REACTIONS = [
        ('Like', 'Like'), ('Love', 'Love'),
        ('Curious', 'Curious'), ('Haha', 'Haha'),
        ('Sad', 'Sad'), ('Angry', 'Angry')
    ]

    reaction = models.CharField(
        help_text='react to a object', max_length=7, choices=REACTIONS)

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created']


class BaseDataModel(models.Model):
    """
    Base data model.

    BaseDataModel acts as an abstract class inherits from
    class Model. Extends your models of this class to add
    the following fields:
        + slugname (SlugField): Store the slugname.
        + about (TextField): Store the about
        + official_web (URLField): Store the oficial web site 
    """

    slugname = models.SlugField(unique=40)

    about = models.TextField(
        help_text='write about something', blank=True)

    official_web = models.URLField(
        help_text='Web site', max_length=200, blank=True)

    class Meta:
        """Meta option."""
        abstract = True