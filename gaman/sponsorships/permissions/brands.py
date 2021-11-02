"""Brand permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsBrandOwner(BasePermission):
    """Allow access only to owner of the brand."""

    def has_object_permission(self, request, view, obj):
        """Check that requesting user is owner of the obj."""
        return request.user == obj.sponsor


class IsProfileCompleted(BasePermission):
    """Allow access only user with profile data completed."""

    message = 'Complete your profile and user data.'

    def has_permission(self, request, view):
        """Check that requesting user has profile and user data completed."""
        user = request.user
        profile = request.user.profile
        return user.is_data_completed() and profile.is_data_completed()