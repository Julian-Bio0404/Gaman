"""Comment model."""

# Django 
from django.db import models

# Managers
from gaman.posts.managers import PrincipalCommentManager, ReplyManager

# Utilities
from gaman.utils.models import GamanModel


class Comment(GamanModel):
    """Comment model."""

    # Type choices
    TYPE = [
        ('Principal-Comment', 'Principal-Comment'),
        ('Reply', 'Reply')
    ]

    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    text = models.TextField(help_text='write a comment', max_length=250)
    reactions = models.PositiveBigIntegerField(default=0)

    replies = models.ManyToManyField(
        'posts.Comment', 
        help_text='Replies of the comment.', related_name='responses', blank=True)

    type = models.CharField(max_length=17, choices=TYPE)

    def __str__(self):
        """Return username, post about and comment."""
        return f'@{self.author} has commented: {self.text} on {self.post}'

    class Meta:
        """Meta options."""
        ordering = ['reactions', 'created']


class PrincipalComment(Comment):
    """Principal Comment proxy model."""

    objects = PrincipalCommentManager()
        
    class Meta:
        """Meta options."""
        ordering = ['reactions', 'created']
        proxy = True


class Reply(Comment):
    """Reply proxy model."""

    objects = ReplyManager()

    class Meta:
        """Meta options."""
        ordering = ['created']
        proxy = True