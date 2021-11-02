"""Follow request permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsFollowedUser(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_permission(self, request, view):
        """Check user requested and user are the same."""
        return request.user == view.user

    def has_object_permission(self, request, view, obj):
        """Check user requested and followed are the same."""
        return request.user == obj.followed


class IsFollowerOrFollowed(BasePermission):
    """Allow access only user follower or user followed."""

    def has_object_permission(self, request, view, obj):
        """Check that request user is follower or followed."""
        return request.user in [obj.followed, obj.follower]