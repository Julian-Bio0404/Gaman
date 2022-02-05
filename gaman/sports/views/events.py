"""Sport Event views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

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

    queryset = SportEvent.objects.all()
    serializer_class = SportEventModelSerializer

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
        assistants = event.assistants.all()
        data = AssistantModelSerializer(assistants, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class SportEventClubViewSet(viewsets.ModelViewSet):
    """
    Sport Event Club viewset.
    Handle create, retrieve, list, update and destroy
    a sport event from a club.
    """

    serializer_class = SportEventModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsClubOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_queryset(self):
        """Return club events."""
        return SportEvent.objects.filter(club=self.club)

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
