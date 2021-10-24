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
                                     IsFollowerPostOwner)

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
    Handle list, create, detail, update, destroy, reply,
    react comment or list comment's reactions.
    """

    serializer_class = CommentModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the post exists."""
        id = kwargs['id']
        self.object = get_object_or_404(Post, id=id)
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
            comments = PrincipalComment.objects.filter(post=self.object)
        else:
            comments = Comment.objects.filter(post=self.object)
        return comments

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in [
            'create', 'retrieve', 'react', 'reactions', 'reply', 'replies']:
            permissions = [IsAuthenticated, IsFollowerPostOwner]
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
        """Handles comment's reaction creation."""
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

    @action(detail=True, methods=['get'])
    def reactions(self, request, *args, **kwargs):
        """List all comment's reactions."""
        comment = self.get_object()
        reactions = CommentReaction.objects.filter(comment=comment)
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

    @action(detail=True, methods=['get'])
    def replies(self, request, *args, **kwargs):
        """List all replies to a comment."""
        comment = self.get_object()
        replies = comment.replies.all()
        data = ReplyModelSerializer(replies, many=True).data
        return Response(data, status=status.HTTP_200_OK)