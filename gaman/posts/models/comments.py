"""Comment model."""

# Django 
from django.db import models

# Utilities
from gaman.utils.models import BaseComment


class Comment(BaseComment):
    """Comment model."""

    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    replies = models.ManyToManyField(
        'posts.Reply', 
        help_text='Replies of the comment.', related_name='replies', blank=True)

    def __str__(self):
        """Return username, post about and comment."""
        return f'@{self.author} has commented: {self.text} on {self.post}'

    class Meta:
        """Meta options."""
        ordering = ['reactions', 'created']


class Reply(BaseComment):
    """Reply model."""

    author = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        """Return username, post about and comment."""
        return f'@{self.author} has replied to your comment'
        
    class Meta:
        """Meta options."""
        verbose_name = 'reply'
        verbose_name_plural = 'replies'
        ordering = ['created']