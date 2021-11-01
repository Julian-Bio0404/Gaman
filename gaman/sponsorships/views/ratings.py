"""Ratings views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from gaman.sponsorships.models import Rating, Sponsorship

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