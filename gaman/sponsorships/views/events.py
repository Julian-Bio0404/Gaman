"""Brand Sport Event views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import IsBrandOwner
from gaman.sports.permissions import IsEventCreator

# Models
from gaman.sponsorships.models import Brand
from gaman.sports.models import SportEvent

# Serializers
from gaman.sports.serializers import (SportEventModelSerializer,
                                      CreateSportEventSerializer)


class SportEventBrandViewSet(viewsets.ModelViewSet):
    """
    Sport Event Brand viewset.
    Handle create, retrieve, list, update and destroy
    a sport event from a brand.
    """

    serializer_class = SportEventModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsEventCreator]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_queryset(self):
        """Return brand events."""
        return SportEvent.objects.filter(brand=self.brand)

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        self.brand = get_object_or_404(Brand, slugname=kwargs['slugname'])
        return super(SportEventBrandViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Handle sport event creation of a brand."""
        serializer = CreateSportEventSerializer(
            data=request.data, context={'author': self.brand})
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = SportEventModelSerializer(event).data
        return Response(data, status=status.HTTP_201_CREATED)
