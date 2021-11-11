"""Clubs views."""

# Django REST Framawork
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sports.permissions import IsClubOwner, IsTrainer

# Models
from gaman.sports.models import Club
from gaman.users.models import FollowUp

# Serializers
from gaman.sports.serializers import ClubModelSerializer, CreateClubSerializer
from gaman.users.serializers import FollowerSerializer


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

    @action(detail=True, methods=['get'])
    def followers(self, request, *args, **kwargs):
        club = self.get_object()
        followers = FollowUp.objects.filter(club=club)
        data = FollowerSerializer(followers, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwargs):
        """Follow or unfollow a club."""
        club = self.get_object()

        # Unfollow
        followup = FollowUp.objects.filter(club=club, follower=request.user)
        if followup.exists():
            followup.delete()
            data = {
                'message': f'you stopped following to {club.slugname}'}
        # Follow
        else:
            FollowUp.objects.create(club=club, follower=request.user)
            data = {'message': f'You started following to {club.slugname}'}
        return Response(data, status=status.HTTP_200_OK)