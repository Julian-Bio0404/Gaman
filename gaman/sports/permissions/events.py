"""Sport Events permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsEventCreator(BasePermission):
    """Allow access only to event creator."""
    
    def has_object_permission(self, request, view, obj):
        """Check requesting user and event creator are the same."""
        return request.user == obj.normalize_author()
