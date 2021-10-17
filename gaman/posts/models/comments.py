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

    comment = models.ForeignKey(
        'self', help_text='Comment that is being replied.',
        on_delete=models.SET_NULL, null=True, related_name='principal_comment')

    def __str__(self):
        """Return username, post about and comment."""
        return f'@{self.author} has commented: {self.text} on {self.post.about}'

    class Meta:
        """Meta options."""
        ordering = ['reactions', 'created']