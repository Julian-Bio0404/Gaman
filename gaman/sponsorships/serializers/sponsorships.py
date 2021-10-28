"""Sponsorships serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sponsorships.models import Sponsorship


class SponsorshipModelSerializer(serializers.ModelSerializer):
    """Sponsorship model serializer."""

    sponsor = serializers.StringRelatedField(read_only=True)
    brand = serializers.StringRelatedField(read_only=True, required=False)

    athlete = serializers.StringRelatedField(read_only=True, required=False)
    club = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        """Meta options."""
        model = Sponsorship
        fields = [
            'sponsor', 'brand',
            'athlete', 'club',
            'start', 'finish',
            'active'
        ]

        read_only_fields = [
            'sponsor', 'brand',
            'athlete', 'club',
            'start', 'finish',
        ]