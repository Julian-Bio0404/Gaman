"""Sport Event views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.response import Response

# Models
from gaman.sports.models import SportEvent

# Serializers
from gaman.sports.serializers import (SportEventModelSerializer,
                                      CreateSportEventSerializer)


class SportEventViewSet(viewsets.ModelViewSet):
    """
    Sport Event Viewset.
    Hnadle create, retrieve, list, update and destroy
    a sport event.
    """

    queryset = SportEvent.objects.all()
    serializer_class = SportEventModelSerializer

    def create(self, request):
        """Handle sport event creation."""
        serializer = CreateSportEventSerializer(
            data=request.data, context={'author': request.user})
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = SportEventModelSerializer(event).data
        return Response(data, status=status.HTTP_201_CREATED)
