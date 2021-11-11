"""Clubs views."""

# Django REST Framawork
from rest_framework import status, viewsets
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from gaman.posts import permissions

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sports.permissions import IsClubOwner, IsTrainer

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
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slugname',)
    ordering_fields = ('slugname',)
    ordering = ('slugname', 'members__count')
    filter_fields = (
        'league__slugname', 'league__state', 'league__sport', 'city')

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['create']:
            permissions = [IsAuthenticated, IsTrainer]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsClubOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def create(self, request):
        """Handles the club creation."""
        serializer = CreateClubSerializer(
            data=request.data, context={'trainer': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)