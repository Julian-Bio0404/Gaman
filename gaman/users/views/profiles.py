"""Profiles views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from gaman.users.permissions import IsProfileOwner

# Models
from gaman.posts.models import Post
from gaman.users.models import Profile

# Serializers
from gaman.posts.serializers import PostModelSerializer
from gaman.users.serializers import (FollowRequestModelSerializer,
                                     ProfileModelSerializer,
                                     UserModelSerializer)


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    Profile viewset.
    Handle profile update, partial update, retrieve and list profile,
    as well as follow, the list of followers and followed.
    """

    queryset = Profile.objects.filter(user__verified=True)
    serializer_class = ProfileModelSerializer
    lookup_field = 'user__username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['retrieve']:
            permissions = [AllowAny]
        elif self.action in ['update', 'partial_update']:
           permissions = [IsAuthenticated, IsProfileOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    @action(detail=True, methods=['get'])
    def posts(self, request, *args, **kwargs):
        """
        List profile's posts. 
        Restric according to the user requesting and privacy of posts.
        """
        profile = self.get_object()
        followers = profile.followers.all()

        if request.user.profile == profile or request.user in followers:
            posts = Post.objects.filter(author=profile.user)
        else:
            posts = Post.objects.filter(author=profile.user, privacy='Public')
        data = PostModelSerializer(posts, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, *args, **kwargs):
        """List all followers."""
        profile = self.get_object()
        followers = profile.followers.all()
        data = UserModelSerializer(followers, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def following(self, request, *args, **kwargs):
        """List all following."""
        profile = self.get_object()
        following = profile.following.all()
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