"""Brands views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import (IsBrandOwner,
                                            IsProfileCompleted,
                                            IsSponsor)

# Models
from gaman.sponsorships.models import Brand
from gaman.users.models import FollowUp

# Serializers
from gaman.sponsorships.serializers import BrandModelSerializer, CreateBrandSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """
    Brand viewset.
    Handle list, create, update, destroy
    retrieve and follow Brand.
    """

    queryset = Brand.objects.all()
    lookup_field = 'slugname'

    def get_permissions(self):
        """Asign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsBrandOwner)
        elif self.action in ['create']:
            permissions.append(IsProfileCompleted)
            permissions.append(IsSponsor)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Add sponsor to serializer context."""
        context = super(BrandViewSet, self).get_serializer_context()
        context['sponsor'] = self.request.user
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateBrandSerializer
        return BrandModelSerializer

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwarg):
        """Handle the follow-up to brand."""
        brand = self.get_object()
        follower = request.user
        followup = FollowUp.objects.filter(follower=follower, brand=brand)
        if followup.exists():
            followup.delete()
            data = {'message': 'You stopped follow to this brand.'}
        else:
            FollowUp.objects.create(follower=follower, brand=brand)
            data = {'message': 'You started follow to this brand.'}
        return Response(data=data, status=status.HTTP_200_OK)