"""Sport Event views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from gaman.sports.models import Club, SportEvent

# Serializers
from gaman.sports.serializers import (SportEventModelSerializer,
                                      CreateSportEventSerializer)


class SportEventViewSet(viewsets.ModelViewSet):
    """
    Sport Event Viewset.
    Handle create, retrieve, list, update and destroy
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


class SportEventClubViewSet(viewsets.ModelViewSet):
    """
    Sport Event Club viewset.
    Handle create, retrieve, list, update and destroy
    a sport event from a club.
    """

    serializer_class = SportEventModelSerializer

    def get_queryset(self):
        """Return club events."""
        return SportEvent.objects.filter(club=self.club)

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        self.club = get_object_or_404(Club, slugname=kwargs['slugname'])
        return super(SportEventClubViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request):
        """Handle sport event creation."""
        serializer = CreateSportEventSerializer(
            data=request.data, context={'author': self.club})
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = SportEventModelSerializer(event).data
        return Response(data, status=status.HTTP_201_CREATED)
