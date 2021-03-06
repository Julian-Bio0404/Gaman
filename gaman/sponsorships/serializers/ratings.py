"""Ratings serializers"""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sponsorships.models import Rating

# Serializer
from .sponsorships import SponsorshipModelSerializer


class RatingSumaryModelserializer(serializers.ModelSerializer):
    """
    Rating sumary model serializer.
    It is used when list ratings of a sponsorship.
    """

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
    """
    Create Rating serializer.
    Handles the creation of a rating.
    """

    comment = serializers.CharField(min_length=30, max_length=250)
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, min_value=1.0, max_value=10.0)

    def validate(self, data):
        """Verify that the rater has not yet rated."""
        rating = Rating.objects.filter(
            qualifier=self.context['qualifier'],
            sponsorship=self.context['sponsorship'])
        if rating.exists():
            raise serializers.ValidationError('You already rated this sponsorship.')
        data['qualifier'] = self.context['qualifier']
        data['sponsorship'] = self.context['sponsorship']
        return data

    def create(self, data):
        """Create a rating."""
        return Rating.objects.create(**data)
