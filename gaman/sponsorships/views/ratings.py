"""Ratings views."""

# Django REST framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Persmissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import IsQualifier, IsSponsored

# Models
from gaman.sponsorships.models import Sponsorship

# Serializers
from gaman.sponsorships.serializers import (CreateRatingSerializer,
                                            RatingModelSerializer,
                                            RatingSumaryModelserializer)


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    Rating view set.
    Handle list, create, retrieve, update,
    rating of the a sponsorship.
    """

    def dispatch(self, request, *args, **kwargs):
        """Verify that the post exists."""
        self.sponsorship = get_object_or_404(Sponsorship, id=kwargs['id'])
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
        if self.action == 'list':
            return RatingSumaryModelserializer
        elif self.action == 'create':
            return CreateRatingSerializer
        return RatingModelSerializer