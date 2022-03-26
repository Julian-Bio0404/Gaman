"""Comments views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.posts.permissions import (IsCommentOwner,
                                     IsCommentOrPostOwner,
                                     IsFollower)

# Models
from gaman.posts.models import (Comment,
                                CommentReaction, Post,
                                PrincipalComment)

# Serializers
from gaman.posts.serializers import (CommentModelSerializer,
                                     CommentReactionModelSerializer,
                                     ReplyModelSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment view set.
    Handles list, create, detail, update, destroy, reply,
    react comment or list comment's reactions and replies.
    """

    serializer_class = CommentModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the post exists."""
        self.object = get_object_or_404(Post, id=kwargs['id'])
        return super(CommentViewSet, self).dispatch(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Delete a comment and its replies."""
        self.object.comments -= instance.replies.all().count() + 1
        self.object.save()
        instance.replies.all().delete()
        instance.delete()

    def get_queryset(self):
        """Return post's comments."""
        if self.action in ['list', 'retrieve', 'reply', 'replies']:
            return PrincipalComment.objects.filter(
                post=self.object).select_related(
                    'author').prefetch_related('replies')
        return Comment.objects.filter(post=self.object).select_related('author')

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'create', 'retrieve', 'list',
                'react', 'reactions', 'reply', 'replies']:
            permissions = [IsAuthenticated, IsFollower]
        elif self.action in ['update', 'partial_update']:
            permissions = [IsAuthenticated, IsCommentOwner]
        elif self.action in ['destroy']:
            permissions = [IsAuthenticated, IsCommentOrPostOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def create(self, request, *args, **kwargs):
        """Handles comment creation."""
        serializer = CommentModelSerializer(
            data=request.data,
            context={'author': request.user, 'post': self.object})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def react(self, request, *args, **kwargs):
        """Handles the creation or deletion of comment's reaction."""
        comment = self.get_object()
        serializer = CommentReactionModelSerializer(
            data=request.data,
            context={'user': request.user, 'comment': comment})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AssertionError:
            data = {'message': "The comment's reaction has been delete."}
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def reactions(self, request, *args, **kwargs):
        """List all comment's reactions."""
        comment = self.get_object()
        reactions = CommentReaction.objects.filter(
            comment=comment).select_related('user')
        serializer = CommentReactionModelSerializer(reactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reply(self, request, *args, **kwargs):
        """Reply to a comment."""
        comment = self.get_object()
        serializer = ReplyModelSerializer(
            data=request.data,
            context={'author': request.user, 'post': self.object, 'comment': comment})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True)
    def replies(self, request, *args, **kwargs):
        """List all replies to a comment."""
        comment = self.get_object()
        replies = comment.replies.all().select_related('author')
        data = ReplyModelSerializer(replies, many=True).data
        return Response(data, status=status.HTTP_200_OK)
