"""SportEvent serializers."""

# Utilities
from datetime import date

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sports.models import SportEvent, Club
from gaman.users.models.users import User

# Utils
from gaman.utils.services import get_ubication


class SportEventModelSerializer(serializers.ModelSerializer):
    """SportEvent model serializer."""

    author = serializers.StringRelatedField(read_only=True, source='specify_author')
    start = serializers.DateField()
    finish = serializers.DateField()

    class Meta:
        """Meta options."""
        model = SportEvent
        fields = [
            'pk', 'author', 'title',
            'description', 'photo',
            'start', 'finish',
            'geolocation', 'country',
            'state', 'city', 'place',
            'created', 'updated'
        ]

        read_only_fields = [
            'pk', 'author', 'geolocation',
            'country', 'state', 'city',
            'created', 'updated'
        ]
    
    def update(self, instance, data):
        """
        Update Sport Event, if the place needs to be
        updated, country, state, city and geolocation
        will also be updated.
        """
        start = data.get('start', None)
        finish = data.get('finish', None)

        if start:
            today = date.today()
            if start < today:
                raise serializers.ValidationError('The start date be must after that current date.')
            if start > instance.finish and not finish:
                raise serializers.ValidationError('The start date be must after that finish date.')

        if finish:
            today = date.today()
            if finish < today:
                raise serializers.ValidationError('The finish date be must after that current date.')
            if finish < instance.start and not start:
                raise serializers.ValidationError('The finish date be must after that start date.')

        if start and finish:
            if start > finish:
                raise serializers.ValidationError('The start date be must before that finish date.')

        ubication = data.get('place', None)
        if ubication:
            ubication = get_ubication(data['place'])
            instance.country = ubication['country']
            instance.state = ubication['state']
            instance.city = ubication['city']
            instance.place = ubication['place']
            instance.geolocation = ubication['geolocation']
        return super().update(instance, data)


class CreateSportEventSerializer(serializers.ModelSerializer):
    """Create Sport Event serializer."""

    author = serializers.StringRelatedField(read_only=True, source='specify_author')
    start = serializers.DateField()
    finish = serializers.DateField()

    class Meta:
        """Meta options."""
        model = SportEvent
        fields = [
            'author', 'title',
            'description', 'photo',
            'start', 'finish', 'place',
            'created', 'updated'
        ]

    def validate(self, data):
        """Check that the start date is before the end date"""
        today = date.today()
        if data['start'] < today or data['finish'] < today:
            raise serializers.ValidationError('The dates be must after that current date.')

        if data['start'] > data['finish']:
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
    