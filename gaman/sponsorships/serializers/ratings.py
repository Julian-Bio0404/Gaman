"""Ratings serializers"""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sponsorships.models import Rating

# Serializer
from .sponsorships import SponsorshipModelSerializer


class RatingModelSerializer(serializers.ModelSerializer):
    """Rating model serializer."""

    sponsorship = SponsorshipModelSerializer(read_only=True)
    qualifier = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Rating
        fields = [
            'sponsorship', 'qualifier',
            'comment', 'rating', 
            'created'
        ]

        read_only_fields = [
            'sponsorship', 'qualifier',
            'created'
        ]