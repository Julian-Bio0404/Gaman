"""Ratings permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from gaman.sports.models import Member


class IsQualifier(BasePermission):
    """Allow access only to qualifier of the sponsorship."""

    def has_object_permission(self, request, view, obj):
        """Check that requesting user is the qualifier."""
        return request.user == obj.qualifier


class IsSponsored(BasePermission):
    """Allow access only users that are sponsored by sponsorship."""

    def has_permission(self, request, view):
        """
        Check that requesting user is a individual
        athlete sponsored or belongs or is a trainer
        of the club sponsored.
        """
        
        if view.sponsorship.athlete:
            return request.user == view.sponsorship.athlete
        else:
            member = Member.objects.filter(
                user=request.user, club=view.sponsorship.club)
            return member.exists() or request.user == view.sponsorship.club.trainer