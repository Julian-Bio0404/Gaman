"""Leagues views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

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


class LeagueDetailView(RetrieveAPIView):
    """
    League Detail view.
    Handles the retrieve league.
    """

    queryset = League.objects.all()
    serializer_class = LeagueModelSerializer
    lookup_field = 'slugname'