"""Sponsorship permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsSponsor(BasePermission):
    """Allow access only to sponsors."""

    message = 'You are not a sponsor.'

    def has_permission(self, request, view):
        """Check that requesting user is a sponsor."""
        user = request.user
        return user.role == 'Sponsor'