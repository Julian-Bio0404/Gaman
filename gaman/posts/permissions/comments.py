"""Comment permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsCommentOwner(BasePermission):
    """Allow access only to comment owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user and comment owner are the same."""
        return request.user == obj.user


class IsCommentOrPostOwner(BasePermission):
    """Allow access only to comment or post owner."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is comment owner or post owner."""
        if request.user == obj.user or request.user == obj.post.user:
            return True
        else:
            return False


class IsFollowerPostOwner(BasePermission):
    """Allow access only to followers of the post owner."""

    def has_object_permission(self, request, view, obj):
        """Check privacy obj and if user is friend of the post owner. """
        post_owner = obj.post.user
        followers = post_owner.profile.followers.all()
        
        if obj.post.privacy == 'Public':
            return True
        elif obj.post.privacy == 'Private':
            if request.user in followers or request.user == post_owner:
                return True
            else:
                return False