"""Follow Request serializers."""

# Django
from django.db.models import Q

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.users.models import FollowRequest, FollowUp


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
    
    def validate(self, data):
        """Verify friend request """
        follower = self.context['follower']
        followed = self.context['followed']

        follow_request = FollowRequest.objects.filter(
            Q (follower=follower, followed=followed) |
            Q (followed=follower, follower=followed))

        if follow_request.exists():
            raise serializers.ValidationError(
                'You already have a follow up request.')
        return data

    def create(self, data):
        """Create a follow request."""
        follower = self.context['follower']
        followed = self.context['followed']
        follow_request = FollowRequest.objects.create(
            follower=follower, followed=followed)
        return follow_request


class AcceptFollowRequestSerializer(serializers.Serializer):
    """Accept Follow Request serializer."""

    accepted = serializers.BooleanField()

    def validate(self, data):
        """Check accepted field."""
        if data['accepted'] != True:
            raise serializers.ValidationError('Follow request not accepted.')
        return data
            
    def save(self):
        """Accept friend request."""
        # Follow request
        follow_request = self.context['follow_request']
        follow_request.accepted = True
        follow_request.save()

        # Create FollowUp
        FollowUp.objects.create(
            follower=follow_request.follower, user=follow_request.followed)


class FollowingSerializer(serializers.ModelSerializer):
    """Following model serializer."""

    user = serializers.StringRelatedField(read_only=True, required=False)
    brand = serializers.StringRelatedField(read_only=True, required=False)
    club = serializers.StringRelatedField(read_only=True, required=False)

    class Meta:
        """Meta options."""
        model = FollowUp
        fields = ['user', 'brand', 'club']
        read_only_fields = ['user', 'brand', 'club']


class FollowerSerializer(serializers.ModelSerializer):
    """Follower model serializer."""

    follower = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = FollowUp
        fields = ['follower']
        read_only_fields = ['follower']