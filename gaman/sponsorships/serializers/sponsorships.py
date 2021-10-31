"""Sponsorships serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sponsorships.models import Brand, Sponsorship
from gaman.sports.models import Club
from gaman.users.models import User


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
            'active'
        ]


class CreateSponsorshipSerializer(serializers.Serializer):
    """Create Sponsorship serializer."""

    brand = serializers.CharField(required=False)
    athlete = serializers.CharField(required=False)
    club = serializers.CharField(required=False)

    start = serializers.DateField()
    finish = serializers.DateField()
    active = serializers.BooleanField(read_only=True)

    def validate(self, data):
        """Verify brand, athlete, club and dates."""
        if 'athlete' in data.keys():
            try:
                athlete = User.objects.get(username=data['athlete'])
                self.context['athlete'] = athlete
                data.pop('athlete')
            except User.DoesNotExist:
                raise serializers.ValidationError('The user does not exists.')
        elif 'club' in data.keys():
            try:
                club = Club.objects.get(slugname=data['club'])
                self.context['club'] = club
                data.pop('club')
            except Club.DoesNotExist:
                raise serializers.ValidationError('The club does not exists.')

        if 'brand' in data.keys():
            try:
                brand = Brand.objects.get(slugname=data['brand'])
                if brand.sponsor != self.context['sponsor']:
                    raise serializers.ValidationError('You are not the owner this brand.')
                self.context['brand'] = brand
                data.pop['brand']
            except Brand.DoesNotExist:
                raise serializers.ValidationError('The brand does not exists.')

        if data['start'] > data['finish']:
            raise serializers.ValidationError(
                'The start date be must before that the finish date.')
        return data

    def create(self, data):
        """Create a sponsorship."""
        sponsor = self.context['sponsor']
        if 'athlete' in self.context.keys():
            athlete = self.context['athlete']
            sponsorship = Sponsorship.objects.create(sponsor=sponsor, athlete=athlete, **data)
        elif 'club' in self.context.keys():
            club = self.context['club']
            sponsorship = Sponsorship.objects.create(sponsor=sponsor, club=club, **data)
        
        if 'brand' in self.context.keys():
            brand = self.context['brand']
            sponsorship.brand = brand
            sponsorship.save()
        return sponsorship