"""League serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sports.models import League


class LeagueModelSerializer(serializers.ModelSerializer):
    """League model serializer."""

    class Meta:
        """Meta options."""
        model = League
        fields = [
            'slugname', 'country',
            'state', 'sport',
            'photo', 'cover_photo',
            'about', 'official_web'
        ]

        read_only_fields = [
            'slugname', 'country',
            'state', 'sport'
        ]