"""Sponsorships views."""

# Django REST Framawork
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from gaman.sponsorships.models import Sponsorship

# Serializers
from gaman.sponsorships.serializers import CreateSponsorshipSerializer, SponsorshipModelSerializer


class SponsorshipViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Saponsorship viewset.
    Handle create, destroy and retrieve sponsorship.
    """

    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipModelSerializer

    def create(self, request):
        """Handle sponsorship creation."""
        print(request.data)
        serializer = CreateSponsorshipSerializer(
            data=request.data, context={'sponsor': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)