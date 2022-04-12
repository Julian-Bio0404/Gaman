"""Reactions models."""

# Django
from django.db import models

# Models
from gaman.utils.models import Reaction


class PostReaction(Reaction):
    """Post Reaction model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    def __str__(self):
        """Return username."""
        return f'@{self.user} reacted to your post.'


class CommentReaction(Reaction):
    """Comment Reaction model."""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE)

    def __str__(self):
        """Return username."""
        return f'@{self.user} reacted to your comment.'
