"""Posts views."""

# Django
from django.db.models import Q

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.posts.permissions import IsFollower, IsPostOwner

# Models
from gaman.posts.models import Post, PostReaction

# Serializers
from gaman.posts.serializers import (PostModelSerializer,
                                     PostReactionModelSerializer,
                                     SharePostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Post viewset.
    Handle list, create, update, destroy, sharing,
    react to a post and list post's reactions.
    """

    serializer_class = PostModelSerializer

    def get_queryset(self):
        """Restrict posts to only followed users."""
        queryset = Post.objects.all()
        user = self.request.user
        following = user.profile.following.all()
        if self.action == 'list':
            queryset = Post.objects.filter(
                Q(author=user) | Q(author__in=following))
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'retrieve', 'react', 'reactions', 'share']:
            permissions = [IsFollower]
        elif self.action in ['update', 'partial_update', 'destroy']:
           permissions = [IsAuthenticated, IsPostOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def create(self, request):
        """Handles post creation."""
        serializer = PostModelSerializer(
            data=request.data, context={'author': request.user, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def react(self, request, *args, **kwargs):
        """Handles post's reaction."""
        post = self.get_object()
        serializer = PostReactionModelSerializer(
            data=request.data, context={'user': request.user, 'post': post})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AssertionError:
            data = {'message': 'The reaction has been delete.'}
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def reactions(self, request, *args, **kwargs):
        """List all post's reactions."""
        post = self.get_object()
        reactions = PostReaction.objects.filter(post=post)
        data = PostReactionModelSerializer(reactions, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def share(self, request, *args, **kwargs):
        """Handles share post."""
        post = self.get_object()
        if post.post != None:
            post = post.post
        serializer = SharePostSerializer(
            data=request.data, context={'author': request.user, 'post': post})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)