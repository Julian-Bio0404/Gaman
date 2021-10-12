"""Profiles views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from gaman.users.models import Profile

# Serializers
from gaman.users.serializers import ProfileModelSerializer
from gaman.users.serializers.users import UserModelSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Profile view set."""

    queryset = Profile.objects.filter(user__verified=True)
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'

    @action(detail=True, methods=['get'])
    def followers(self, request, *args, **kwargs):
        """List all followers."""
        profile = self.get_object()
        followers = profile.followers
        data = UserModelSerializer(followers, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def following(self, request, *args, **kwargs):
        """List all following."""
        profile = self.get_object()
        following = profile.following
        data = UserModelSerializer(following, many=True).data
        return Response(data, status=status.HTTP_200_OK)