"""Post models."""

# Django
from django.db import models

# Utils
from gaman.utils.models import GamanModel


class Post(GamanModel):
    """Post model."""

    # Post privacy choices
    PRIVACY = [
        ('Public', 'Public'),
        ('Private', 'Private')
    ]

    # post feeling choices
    FEELING = [
        ('Happy', 'Happy'), ('Loved', 'Loved'),
        ('Excited', 'Excited'), ('Crazy', 'Crazy'),
        ('Thankful', 'Thankful'), ('Fantastic', 'Fantastic'),
        ('Motived', 'Motived'), ('Tired', 'Tired'),
        ('Alone', 'Alone'), ('Angry', 'Angry'),
        ('Sorry', 'Sorry'), ('Confused', 'Confused'),
        ('Strong', 'Strong'), ('Stressed', 'Stressed'),
        ('Scared', 'Scared'), ('Sick', 'Sick'),
        ('Sarcastic', 'Sarcastic'), ('Anxious', 'Anxious'),
        ('Nostalgic', 'Nostalgic'), ('Proud', 'Proud'), 
        ('Curious', 'Curious'), ('Surprised', 'Surprised')
    ]

    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    about = models.TextField(help_text='Write something', blank=True)

    privacy = models.CharField(
        help_text="Post's Privacy", max_length=7, choices=PRIVACY, default='Public')

    location = models.CharField(help_text='Where are you?', max_length=60, blank=True)

    pictures = models.ManyToManyField('Picture', blank=True)
    videos = models.ManyToManyField('Video', blank=True)

    feeling = models.CharField(
        help_text='How you feel?', max_length=9, choices=FEELING, blank=True)
    
    tag_friends = models.ManyToManyField(
        'users.User', blank=True, related_name='tag_friends')

    post = models.ForeignKey(
        'self', help_text='Post to be republished.', on_delete=models.SET_NULL, null=True, related_name='re_post')
    
    reactions = models.PositiveBigIntegerField(default=0)
    comments = models.PositiveBigIntegerField(default=0)
    shares = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        """Return about and username."""
        return f'{self.about} by @{self.author}'