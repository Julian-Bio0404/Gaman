"""Leagues views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from gaman.sports.models import League

# Serializer
from gaman.sports.serializers import LeagueModelSerializer


class LeagueViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    League View.
    Handles the list and retrieve league.
    """

    queryset = League.objects.all()
    serializer_class = LeagueModelSerializer
    lookup_field = 'slugname'
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('slugname',)
    ordering_fields = ('slugname',)
    ordering = ('slugname', 'country', 'state')
    filter_fields = ('country', 'state', 'sport')
