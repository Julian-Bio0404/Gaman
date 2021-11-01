"""Ratings serializers"""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sponsorships.models import Rating

# Serializer
from .sponsorships import SponsorshipModelSerializer


class RatingSumaryModelserializer(serializers.ModelSerializer):
    """Rating sumary model serializer."""

    qualifier = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Rating
        fields = [
            'qualifier', 'comment',
            'rating', 'created'
        ]

        read_only_fields = [
            'qualifier', 'created'
        ]


class RatingModelSerializer(RatingSumaryModelserializer):
    """Rating model serializer."""

    sponsorship = SponsorshipModelSerializer(read_only=True)

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

    def create(self, data):
        """Create a rating."""
        sponsorship = self.context['sponsorship']
        qualifier = self.context['qualifier']
        rating = Rating.objects.create(
            **data, sponsorship=sponsorship, qualifier=qualifier)
        return rating