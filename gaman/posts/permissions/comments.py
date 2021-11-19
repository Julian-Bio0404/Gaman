"""Comment permissions."""

# Django
from django.db.models import Q

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
        return request.user == obj.post.normalize_author()


class IsFollower(BasePermission):
    """Allow access only to followers of the post owner."""

    def has_permission(self, request, view):
        """
        Check privacy post and if user is follower of the
        post owner or if requesting user is the post owner.
        """
        post = view.object
        post_owner = post.normalize_author()
        
        if post.privacy == 'Public' or request.user == post_owner:
            return True
        elif post.privacy == 'Private':
            folloup = FollowUp.objects.filter(
                Q(follower=request.user, user=post_owner ) |
                Q(follower=request.user, brand=post.brand) |
                Q(follower= request.user, club=post.club))
            return folloup.exists()