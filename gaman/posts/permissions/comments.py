"""Comment permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from gaman.users.models import FollowUp


class IsCommentOwner(BasePermission):
    """Allow access only to comment owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and comment owner are the same."""
        return request.user == obj.author


class IsCommentOrPostOwner(BasePermission):
    """Allow access only to comment or post owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is comment owner or post owner."""
        return request.user in [obj.author, obj.post.author]


class IsFollowerPostOwner(BasePermission):
    """Allow access only to followers of the post owner."""

    def has_object_permission(self, request, view, obj):
        """Check privacy obj and if user is friend of the post owner. """
        post_owner = obj.post.author
        
        if obj.post.privacy == 'Public':
            return True
        elif obj.post.privacy == 'Private':
            folloup = FollowUp.objects.filter(
                follower=request.user, user=post_owner)
            if folloup.exists() or request.user == post_owner:
                return True
            else:
                return False