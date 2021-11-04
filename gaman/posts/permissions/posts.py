"""Post permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from gaman.users.models import FollowUp


class IsPostOwner(BasePermission):
    """Allow access only to post owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and post owner are the same."""
        return request.user == obj.author


class IsFollowerOrPostOwner(BasePermission):
    """
    Allow access only to followers of a
    user or to post owner.
    """

    message = 'This content isn`t available right now.'

    def has_object_permission(self, request, view, obj):
        """
        Check privacy post and if user is follower of the
        post owner or if requesting user is the post owner.
        """
        post_owner = obj.author

        if obj.privacy == 'Public' or request.user == post_owner:
            return True
        elif obj.privacy == 'Private':
            folloup = FollowUp.objects.filter(
                follower=request.user, user=post_owner)
            if folloup.exists():
                return True
            return False