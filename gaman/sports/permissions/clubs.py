"""Clubs permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsTrainer(BasePermission):
    """Allow access only to a coach or league president."""

    def has_permission(self, request, view):
        """Check user's role."""
        return request.user.role in ('Coach', 'League president')


class IsClubOwner(BasePermission):
    """Allow access only to owner the club."""

    def has_permission(self, request, view):
        try:
            obj = view.club
        except AttributeError:
            obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Check requesting user is owner of the club."""
        return obj.trainer == request.user