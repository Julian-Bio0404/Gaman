"""Comment model."""

# Django 
from django.db import models

# Utilities
from gaman.utils.models import GamanModel


class Comment(GamanModel):
    """Comment model."""

    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    text = models.TextField(help_text='write a comment', max_length=250)
    reactions = models.PositiveBigIntegerField(default=0)

    replies = models.ManyToManyField(
        'self', help_text='Replies of the comment.',
        blank=True, related_name='replies')

    def __str__(self):
        """Return username, post about and comment."""
        return f'@{self.author} has commented: {self.text} on {self.post}'

    class Meta:
        """Meta options."""
        ordering = ['reactions', 'created']