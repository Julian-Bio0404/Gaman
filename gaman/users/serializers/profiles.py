"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta options."""
        model = Profile
        fields = [
            'photo', 'cover_photo',
            'about', 'birth_date',
            'sport', 'country',
            'web_site', 'social_link'
        ]