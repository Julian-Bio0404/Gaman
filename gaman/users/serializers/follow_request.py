"""Follow Request serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.users.models import FollowRequest


class FollowRequestModelSerializer(serializers.ModelSerializer):
    """Follow Request model serializer."""

    follower = serializers.StringRelatedField(read_only=True)
    followed = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = FollowRequest
        fields = [
            'follower', 'followed',
            'accepted', 'created'
        ]

        read_only_fields = [
            'follower', 'followed',
            'accepted'
        ]