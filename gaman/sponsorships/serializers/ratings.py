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


class CreateRatingSerializer(serializers.Serializer):
    """Create Rating serializer."""

    comment = serializers.CharField(min_length=30, max_length=200)
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, min_value=1.0, max_value=10.0)

    def validate(self, data):
        """Verify that the rater has not yet rated."""
        qualifier = self.context['qualifier']
        sponsorship = self.context['sponsorship']
        rating = Rating.objects.filter(qualifier=qualifier, sponsorship=sponsorship)
        if rating.exists():
            raise serializers.ValidationError('You already rated this sponsorship.')
        return data

    def create(self, data):
        """Create a rating."""
        sponsorship = self.context['sponsorship']
        qualifier = self.context['qualifier']
        rating = Rating.objects.create(
            **data, sponsorship=sponsorship, qualifier=qualifier)
        return rating
