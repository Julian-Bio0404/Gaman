"""SportEvent serializers."""

# Utilities
from datetime import date

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sports.models import SportEvent, Club
from gaman.users.models.users import User

# Serializers
from gaman.users.serializers import ProfileSumaryModelSerializer

# Utils
from gaman.utils.services import get_ubication


class SportEventModelSerializer(serializers.ModelSerializer):
    """SportEvent model serializer."""

    author = serializers.StringRelatedField(
        read_only=True, source='specify_author')

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
        today = date.today()

        if start:
            if start < today:
                raise serializers.ValidationError(
                    'The start date be must after that current date.')
            if start > instance.finish and not finish:
                raise serializers.ValidationError(
                    'The start date be must after that finish date.')

        if finish:
            if finish < today:
                raise serializers.ValidationError(
                    'The finish date be must after that current date.')
            if finish < instance.start and not start:
                raise serializers.ValidationError(
                    'The finish date be must after that start date.')

        if start and finish:
            if start > finish:
                raise serializers.ValidationError(
                    'The start date be must before that finish date.')

        place = data.get('place', None)
        if place:
            ubication = get_ubication(place)
            data.update(ubication)
        return super().update(instance, data)


class CreateSportEventSerializer(serializers.ModelSerializer):
    """Create Sport Event serializer."""

    author = serializers.StringRelatedField(
        read_only=True, source='specify_author')

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
            raise serializers.ValidationError(
                'The dates be must after that current date.')

        if data['start'] > data['finish']:
            raise serializers.ValidationError(
                'The start date be must before that finish date.')
        return data

    def create(self, data):
        """Create a Sport Event."""
        # The author can be a user, club or a brand.
        author = self.context['author']
        author_type = type(author)

        if author_type == User:
            data['user'] = author
        elif author_type == Club:
            data['club'] = author
        else:
            data['brand'] = author

        # Set ubication of the event
        ubication = get_ubication(data['place'])
        data.update(ubication)
        event = SportEvent.objects.create(**data)
        return event


class AssistantModelSerializer(serializers.ModelSerializer):
    """Assitant model serializer."""

    name = serializers.CharField(source='get_full_name')
    profile = ProfileSumaryModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = User
        fields = [
            'username', 'name',
            'profile', 'role'
        ]

        read_only_fields = [
            'username', 'name',
            'profile', 'role'
        ]
