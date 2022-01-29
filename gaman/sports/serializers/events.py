"""SportEvent serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sports.models import SportEvent, Club
from gaman.users.models.users import User

# Utils
from utils.services import get_ubication


class SportEventModelSerializer(serializers.ModelSerializer):
    """SportEvent model serializer."""

    author = serializers.StringRelatedField(read_only=True, source='specify_author')
    start = serializers.DateField()
    finish = serializers.DateField()

    class Meta:
        """Meta options."""
        model = SportEvent
        fields = [
            'author', 'title',
            'description', 'photo',
            'start', 'finish',
            'geolocation', 'country',
            'state', 'city', 'place',
            'created', 'updated'
        ]

        read_only_fields = [
            'author', 'country',
            'state', 'city', 'place',
            'created', 'updated'
        ]
    
    def validate(self, data):
        """Check that the start date is before the end date"""
        if data['start'] >= data['finish']:
            raise serializers.ValidationError(
                'The start date be must before that finish date.')
        return data
    
    def create(self, data):
        """Create a Sport Event."""
        # The author can be a user, club or a brand.
        author = self.context['author']
        if type(author) == User:
            event = SportEvent.objects.create(user=author, **data)
        elif type(author) == Club:
            event = SportEvent.objects.create(club=author, **data)
        else:
            event = SportEvent.objects.create(brand=author, **data)
        
        # Set ubication of the event
        ubication = get_ubication(data['place'])

        event.country = ubication['country']
        event.state = ubication['state']
        event.city = ubication['city']
        event.place = ubication['place']
        event.geolocation = ubication['geolocation']
        event.save()
        return event
    