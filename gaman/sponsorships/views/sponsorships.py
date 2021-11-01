"""Sponsorships views."""

# Django REST Framawork
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sponsorships.permissions import IsProfileCompleted, IsSponsor

# Models
from gaman.sponsorships.models import Sponsorship

# Serializers
from gaman.sponsorships.serializers import (CreateSponsorshipSerializer,
                                            SponsorshipModelSerializer)


class SponsorshipViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Saponsorship viewset.
    Handle create and retrieve sponsorship.
    """

    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipModelSerializer

    def get_permissions(self):
        """Asign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['create']:
            permissions.append(IsSponsor)
            permissions.append(IsProfileCompleted)
        return [p() for p in permissions]

    def create(self, request):
        """Handle sponsorship creation."""
        serializer = CreateSponsorshipSerializer(
            data=request.data, context={'sponsor': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)