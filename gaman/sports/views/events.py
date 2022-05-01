"""Sport Event views."""

# Utilities
from urllib import response
import requests

# Django
from django.conf import settings

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sports.permissions import IsClubOwner, IsEventCreator

# Models
from gaman.sports.models import Club, SportEvent

# Serializers
from gaman.sports.serializers import (AssistantModelSerializer,
                                      CreateSportEventSerializer,
                                      SportEventModelSerializer)


class SportEventViewSet(viewsets.ModelViewSet):
    """
    Sport Event Viewset.
    Handle create, retrieve, list, update and destroy
    a sport event.
    """

    queryset = SportEvent.objects.all().select_related('user', 'brand', 'club')
    serializer_class = SportEventModelSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('country', 'state', 'city')
    ordering_fields = ('start',)
    ordering = ('start',)
    filter_fields = ('country', 'state', 'city')

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsEventCreator]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def create(self, request):
        """Handle sport event creation."""
        serializer = CreateSportEventSerializer(
            data=request.data, context={'author': request.user})
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = SportEventModelSerializer(event).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def go(self, request, *args, **kwargs):
        """Go to an event."""
        event = self.get_object()
        user = request.user
        if user not in event.assistants.all():
            event.assistants.add(user)
            data = {'message': 'You will go to this event.'}
        else:
            event.assistants.remove(user)
            data = {'message': 'You will not go to this event.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def assistants(self, request, *args, **kwargs):
        """List of assistants of the event."""
        event = self.get_object()
        assistants = event.assistants.all().select_related('profile')
        data = AssistantModelSerializer(assistants, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='events-nearby/')
    def events_nearby(self, request):
        """Get events nearby from a geolocation."""
        url = settings.GEOGAMAN_DOMAIN + 'zones/events/'
        response = requests.post(url, request.data)
        if response.status_code == 200:
            ids = response.json()['events_ids']
            events = SportEvent.objects.filter(id__in=ids)
            data = SportEventModelSerializer(events, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(response.content, status=response.status_code)


class SportEventClubViewSet(viewsets.ModelViewSet):
    """
    Sport Event Club viewset.
    Handle create, retrieve, list, update and destroy
    a sport event from a club.
    """

    serializer_class = SportEventModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsEventCreator]
        elif self.action in ['create']:
            permissions = [IsClubOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_queryset(self):
        """Return club events."""
        return SportEvent.objects.filter(club=self.club).select_related('club')

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        self.club = get_object_or_404(Club, slugname=kwargs['slugname'])
        return super(SportEventClubViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Handle sport event creation of a club."""
        serializer = CreateSportEventSerializer(
            data=request.data, context={'author': self.club})
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        data = SportEventModelSerializer(event).data
        return Response(data, status=status.HTTP_201_CREATED)
