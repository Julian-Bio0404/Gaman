"""Ratings views."""

# Django REST framework
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

# Persmissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import IsQualifier, IsSponsored

# Models
from gaman.sponsorships.models import Sponsorship

# Serializers
from gaman.sponsorships.serializers import (RatingModelSerializer,
                                            RatingSumaryModelserializer)


class RatingViewSet(viewsets.ModelViewSet):
    """
    Rating view set.
    Handle list, create, detail, update,
    destroy rating of the a sponsorship.
    """

    serializer_class = RatingModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the post exists."""
        id = kwargs['id']
        self.sponsorship = get_object_or_404(Sponsorship, id=id)
        return super(RatingViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permission based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsQualifier)
        elif self.action == 'create':
            permissions.append(IsSponsored)
        return [p() for p in permissions]

    def get_queryset(self):
        """Filter sponsorship's ratings"""
        ratings = self.sponsorship.rating_set.all()
        return ratings

    def get_serializer_context(self):
        """Add qualifier and sponsorship to serializer context."""
        context = super(RatingViewSet, self).get_serializer_context()
        context['sponsorship'] = self.sponsorship
        context['qualifier'] = self.request.user
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return RatingModelSerializer
        elif self.action == 'list':
            return RatingSumaryModelserializer
        return RatingModelSerializer