"""Sponsorships serializers."""

# Utilities
import datetime

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sponsorships.models import Brand, Sponsorship
from gaman.sports.models import Club
from gaman.users.models import User


class SponsorshipModelSerializer(serializers.ModelSerializer):
    """Sponsorship model serializer."""

    sponsor = serializers.StringRelatedField(read_only=True)

    sponsored = serializers.StringRelatedField(
        read_only=True, source='specify_sponsored')

    class Meta:
        """Meta options."""
        model = Sponsorship
        fields = [
            'sponsor', 'sponsored',
            'start', 'finish',
            'active'
        ]

        read_only_fields = [
            'sponsor', 'sponsored',
            'start', 'finish',
            'active'
        ]


class CreateSponsorshipSerializer(serializers.Serializer):
    """
    Create Sponsorship serializer.
    Handles the creation of sponsorships.
    """

    brand = serializers.CharField(required=False)
    athlete = serializers.CharField(required=False)
    club = serializers.CharField(required=False)

    start = serializers.DateField()
    finish = serializers.DateField()
    active = serializers.BooleanField(read_only=True)

    def validate(self, data):
        """Verify brand, athlete, club and dates."""
        brand = data.get('brand', None)
        athlete = data.get('athlete', None)
        club = data.get('club', None)

        if athlete and club:
            raise serializers.ValidationError('You must choose an athlete or a club, not both')
        elif athlete:
            try:
                data['athlete'] = User.objects.get(username=athlete)
            except User.DoesNotExist:
                raise serializers.ValidationError('The user does not exists.')
        elif club:
            try:
                data['club'] = Club.objects.get(slugname=club)
            except Club.DoesNotExist:
                raise serializers.ValidationError('The club does not exists.')
        else:
            raise serializers.ValidationError('You must choose an athlete or a club.')

        if brand:
            try:
                brand = Brand.objects.get(slugname=brand)
                if brand.sponsor != self.context['sponsor']:
                    raise serializers.ValidationError('You are not the owner this brand.')
                data['brand'] = brand
            except Brand.DoesNotExist:
                raise serializers.ValidationError('The brand does not exists.')

        if data['start'] <= datetime.date.today() or data['finish'] <= datetime.date.today():
            raise serializers.ValidationError(
                'The dates be must after that the current date.')

        if data['start'] >= data['finish']:
            raise serializers.ValidationError(
                'The start date be must before that the finish date.')
        return data

    def create(self, data):
        """Create a sponsorship."""
        sponsor = self.context['sponsor']
        sponsorship = Sponsorship.objects.create(sponsor=sponsor, **data)
        return sponsorship