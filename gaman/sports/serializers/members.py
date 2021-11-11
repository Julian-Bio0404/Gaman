"""Members serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sports.models import Member

# Serializers
from gaman.users.serializers import UserModelSerializer



class MemberModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user = UserModelSerializer(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        """Meta class."""

        model = Member
        fields = [
            'user', 'active',
            'joined_at'
        ]

        read_only_fields = ['user', 'joined_at']