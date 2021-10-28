"""Brands views."""

# Django REST Framework
from rest_framework import viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import IsBrandOwner, IsProfileCompleted

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

    def get_permissions(self):
        """Asign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsBrandOwner)
        elif self.action in ['create']:
            permissions.append(IsProfileCompleted)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Add sponsor to serializer context."""
        context = super(BrandViewSet, self).get_serializer_context()
        context['sponsor'] = self.request.user
        return context
