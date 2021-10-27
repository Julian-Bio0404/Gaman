"""Brands serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sponsorships.models import Brand


class BrandModelSerializer(serializers.ModelSerializer):
    """Brand model seriaizer."""

    sponsor = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Brand
        fields = [
            'slugname', 'about',
            'sponsor', 'photo',
            'cover_photo', 'verified',
            'official_web', 'created'
        ]

        read_only_fields = [
            'sponsor', 'created',
            'verified'
        ]

    def create(self, data):
        """Create a brand."""
        sponsor = self.context['sponsor']
        brand = Brand.objects.create(**data, sponsor=sponsor)
        return brand