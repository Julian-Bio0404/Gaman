"""Post permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsPostOwner(BasePermission):
    """Allow access only to post owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and post owner are the same."""
        return request.user == obj.user


class IsFollower(BasePermission):
    """Allow access only to followers of a user."""

    message = 'This content isn`t available right now.'

    def has_object_permission(self, request, view, obj):
        """Check privacy obj and if user is friend of the post owner. """
        post_owner = obj.user
        followers = post_owner.profile.followers.all()
        
        if obj.privacy == 'Public':
            return True
        elif obj.privacy == 'Private':
            if request.user in followers or request.user == post_owner:
                return True
            else:
                return False