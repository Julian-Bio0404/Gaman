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
        Check that requesting user is a sponsored
        from the sponsorship.
        """
        # Si el patrocinado no es un atleta individual, es un atleta de un club patrocinado
        # Por lo tanto, evalua si es el atleta o pertenece o es el entrenador de dicho club
        if view.sponsorship.athlete != None:
            return request.user == view.sponsorship.athlete
        else:
            member = Member.objects.filter(
                user=request.user, club=view.sponsorship.club)
            if member.exists() or request.user == view.sponsorship.club.trainer:
                return True
            return False