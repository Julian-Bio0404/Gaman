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
    
    def validate(self, data):
        """Verify friend request """
        follower = self.context['follower']
        followed = self.context['followed']

        follow_request = FollowRequest.objects.filter(
            follower=follower, followed=followed)

        if follow_request.exists():
            raise serializers.ValidationError(
                'You already sent a follow up request.')
        else:
            follow_request2 = FollowRequest.objects.filter(
                follower=followed, followed=follower)
            if follow_request2.exists():
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

        # Update user's profile
        follower = follow_request.follower
        followed = follow_request.followed

        follower.profile.following.add(followed)
        followed.profile.followers.add(follower)

        follower.profile.save()
        followed.profile.save()