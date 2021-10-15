"""Profiles views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from gaman.users.models import Profile

# Serializers
from gaman.users.serializers import (FollowRequestModelSerializer,
                                     ProfileModelSerializer, 
                                     UserModelSerializer)


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

    @action(detail=True, methods=['post'])
    def follow(self, request, *args, **kwargs):
        """Follow or unfollow a user."""
        profile = self.get_object()
        followers = profile.followers.all()
        user = request.user

        if request.user == profile.user:
            data = {'message': "You can't follow yourself."}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        # Follow
        if request.user not in followers:
            if profile.public == True:
                profile.followers.add(request.user)
                request.user.profile.following.add(profile.user)
                data = {
                    'message': f'You started following to {profile.user.username}'}
            # Follow Request
            else:
                serializer = FollowRequestModelSerializer(
                    data=request.data,
                    context={'follower': request.user, 'followed': profile.user})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Unfollow
        else:
            profile.followers.remove(user)
            request.user.profile.following.remove(user)
            data = {
                'message': f'you stopped following to {profile.user.username}'}
        profile.save()
        request.user.profile.save()
        return Response(data, status=status.HTTP_200_OK)