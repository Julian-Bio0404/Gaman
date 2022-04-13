"""Profile permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from gaman.users.models import User, FollowUp


class IsProfileOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check obj and profile are the same."""
        return request.user.profile == obj

class IsFollower(BasePermission):

    def has_object_permission(self, request, view, obj):
        """Check that request user is follower or profile owner."""
        user = request.user
        if obj.public:
            return True

        followers = FollowUp.objects.filter(user=obj.user, follower=user)
        return user.profile == obj or followers.exists()
