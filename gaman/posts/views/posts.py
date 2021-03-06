"""Posts views."""

# Django
from django.db.models import Q

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.posts.permissions import IsFollowerOrPostOwner, IsPostOwner

# Models
from gaman.posts.models import Post, PostReaction
from gaman.sponsorships.models import Brand
from gaman.sports.models import Club
from gaman.users.models import FollowUp
from gaman.users.models import User

# Serializers
from gaman.posts.serializers import (PostModelSerializer,
                                     PostReactionModelSerializer,
                                     SharePostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Post viewset.
    Handles list, create, update, destroy, sharing,
    react to a post and list post's reactions.
    """

    serializer_class = PostModelSerializer

    def get_queryset(self):
        """Restrict posts to only followed users."""
        if self.action == 'list':
            followed_users = User.objects.filter(
                pk__in=[FollowUp.objects.filter(
                    follower=self.request.user).values('user__pk')])

            followed_brands = Brand.objects.filter(
                pk__in=[FollowUp.objects.filter(
                    follower=self.request.user).values('brand__pk')])

            followed_clubs = Club.objects.filter(
                pk__in=[FollowUp.objects.filter(
                    follower=self.request.user).values('club__pk')])

            queryset = Post.objects.filter(
                Q(user=self.request.user) |
                Q(user__in=followed_users) |
                Q(brand__in=followed_brands) |
                Q(club__in=followed_clubs)).select_related(
                    'user', 'brand', 'club', 'post'
            ).prefetch_related('pictures', 'videos', 'tag_users')
        else:
            queryset = Post.objects.all().select_related(
                'user', 'brand', 'club', 'post'
            ).prefetch_related('pictures', 'videos', 'tag_users')
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'retrieve', 'react', 'reactions', 'share', 'likes',
                'loves', 'hahas', 'curious', 'sads', 'angry']:
            permissions = [IsAuthenticated, IsFollowerOrPostOwner]
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
        """Handles the creation or deletion of post's reaction."""
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

    @action(detail=True, methods=['post'])
    def share(self, request, *args, **kwargs):
        """Handles share post."""
        post = self.get_object()
        if post.post:
            post = post.post
        serializer = SharePostSerializer(
            data=request.data, context={'author': request.user, 'post': post})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def reactions(self, request, *args, **kwargs):
        """List all post's reactions."""
        post = self.get_object()
        reactions = PostReaction.objects.filter(
            post=post).select_related('user')
        data = {
            'count': reactions.count(),
            'reactions': PostReactionModelSerializer(reactions, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def likes(self, request, *args, **kwargs):
        """List of reactions filtered by like."""
        post = self.get_object()
        likes = post.postreaction_set.filter(
            reaction='Like').select_related('user')
        data = {
            'count': likes.count(),
            'likes': PostReactionModelSerializer(likes, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def loves(self, request, *args, **kwargs):
        """List of reactions filtered by love."""
        post = self.get_object()
        loves = post.postreaction_set.filter(
            reaction='Love').select_related('user')
        data = {
            'count': loves.count(),
            'loves': PostReactionModelSerializer(loves, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def hahas(self, request, *args, **kwargs):
        """List of reactions filtered by haha."""
        post = self.get_object()
        hahas = post.postreaction_set.filter(
            reaction='Haha').select_related('user')
        data = {
            'count': hahas.count(),
            'hahas': PostReactionModelSerializer(hahas, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def curious(self, request, *args, **kwargs):
        """List of reactions filtered by curious."""
        post = self.get_object()
        curious = post.postreaction_set.filter(
            reaction='Curious').select_related('user')
        data = {
            'count': curious.count(),
            'curious': PostReactionModelSerializer(curious, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def sads(self, request, *args, **kwargs):
        """List of reactions filtered by sad."""
        post = self.get_object()
        sads = post.postreaction_set.filter(
            reaction='Sad').select_related('user')
        data = {
            'count': sads.count(),
            'sads': PostReactionModelSerializer(sads, many=True).data}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def angry(self, request, *args, **kwargs):
        """List of reactions filtered by angry."""
        post = self.get_object()
        angrys = post.postreaction_set.filter(
            reaction='Angry').select_related('user')
        data = {
            'count': angrys.count(),
            'angrys': PostReactionModelSerializer(angrys, many=True).data}
        return Response(data, status=status.HTTP_200_OK)
