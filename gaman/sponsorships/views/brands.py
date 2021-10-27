"""Brands views."""

# Django REST Framework
from rest_framework import viewsets

# Models
from gaman.sponsorships.models import Brand

# Serializers
from gaman.sponsorships.serializers import BrandModelSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """
    Brand viewset.
    Handle list, create, update, destroy and
    retrieve Brand.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    lookup_field = 'slugname'

    def get_serializer_context(self):
        """Add sponsor to serializer context."""
        context = super(BrandViewSet, self).get_serializer_context()
        context['sponsor'] = self.request.user
        return context
