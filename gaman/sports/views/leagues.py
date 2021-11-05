"""Leagues views."""

# Django REST Framework
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from gaman.sports.models import League

# Serializer
from gaman.sports.serializers import LeagueModelSerializer


class LeagueListView(ListAPIView):
    """
    League List view.
    Handles list of the leagues.
    """

    queryset = League.objects.all()
    serializer_class = LeagueModelSerializer
    permission_classes = [IsAuthenticated]


class LeagueDetailView(RetrieveAPIView):
    """
    League Detail view.
    Handles the retrieve league.
    """

    queryset = League.objects.all()
    serializer_class = LeagueModelSerializer
    lookup_field = 'slugname'
    permission_classes = [IsAuthenticated]