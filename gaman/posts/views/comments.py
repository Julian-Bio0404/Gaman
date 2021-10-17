"""Comments views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from gaman.posts.models import Comment, CommentReaction, Post

# Serializers
from gaman.posts.serializers import (CommentModelSerializer,
                                     CommentReactionModelSerializer,
                                     CommentReplySerializer)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment view set.
    Handle list, create, detail, update, destroy, 
    react comment or list comment's reactions.
    """
    
    serializer_class = CommentModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the post exists."""
        id = kwargs['id']
        self.object = get_object_or_404(Post, id=id)
        return super(CommentViewSet, self).dispatch(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Delete a comment and subtract -1 from comments on the post."""
        self.object.comments -= 1
        self.object.save()
        instance.delete()
    
    def get_queryset(self):
        """Return post's comments."""
        comments = Comment.objects.filter(post=self.object)
        return comments
    
    def create(self, request, *args, **kwargs):
        """Handles comment creation."""
        serializer = CommentModelSerializer(
            data=request.data,
            context={'user': request.user, 'post': self.object})
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
        serializer = CommentReplySerializer(
            data=request.data,
            context={
                'author': request.user, 
                'post': self.object,'comment': comment})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)