"""Brands serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
            'slugname', 'sponsor',
            'created', 'verified'
        ]


class CreateBrandSerializer(serializers.Serializer):
    """
    Create Brand serializer.
    Handles the creation of a Brand.
    """

    slugname = serializers.CharField(
        min_length=2, max_length=40,
        validators=[UniqueValidator(queryset=Brand.objects.all())])
    
    about = serializers.CharField(min_length=10, max_length=350, required=False)
    photo = serializers.ImageField(required=False)
    cover_photo = serializers.ImageField(required=False)
    official_web = serializers.URLField(required=False)

    def create(self, data):
        """Create a brand."""
        sponsor = self.context['sponsor']
        brand = Brand.objects.create(**data, sponsor=sponsor)
        return brand