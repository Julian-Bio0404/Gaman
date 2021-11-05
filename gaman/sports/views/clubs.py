"""Clubs views."""

# Django REST Framawork
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from gaman.sports import serializers

# Models
from gaman.sports.models import Club

# Serializers
from gaman.sports.serializers import ClubModelSerializer, CreateClubSerializer


class ClubViewSet(viewsets.ModelViewSet):
    """
    Club Viewset.
    Handles create, detail, update and destroy club.
    """

    queryset = Club.objects.all()
    serializer_class = ClubModelSerializer
    lookup_field = 'slugname'

    def create(self, request):
        """Handles the club creation."""
        serializer = CreateClubSerializer(
            data=request.data, context={'trainer': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)