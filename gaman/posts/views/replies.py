"""Replies views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from gaman.posts.models.comments import Reply

# Serializers
from gaman.posts.serializers import (CommentReactionModelSerializer,
                                     ReplyModelSerializer,
                                     ReplyReactionModelSerializer)


class ReplyViewSet(viewsets.ModelViewSet):
    """
    Reply viewset.
    Handle list, create, detail, update, destroy,
    react reply or list reply's reactions.
    """
    serializer_class = ReplyModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the comment exists."""
        id = kwargs['id']
        self.comment = get_object_or_404(Reply, id=id)
        self.object = self.comment.post
        return super(ReplyViewSet, self).dispatch(request, *args, **kwargs)

    def perfom_destroy(self, instance):
        """Delete a reply and substract -1 from comments on the post."""
        self.object.comments -= 1
        self.object.save()
        instance.delete()

    def get_queryset(self):
        """Return comment's replies."""
        replies = self.comment.replies.all()
        return replies

    def create(self, request, *args, **kwargs):
        """Reply to a comment."""
        serializer = ReplyModelSerializer(
            data=request.data,
            context={
                'author': request.user, 
                'post': self.object, 'comment': self.comment})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def react(self, request, *args, **kwargs):
        """Handles comment's reaction creation."""
        reply = self.get_object()
        serializer = ReplyReactionModelSerializer(
            data=request.data,
            context={'user': request.user, 'reply': reply})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AssertionError:
            data = {'message': "The comment's reaction has been delete."}
            return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def reactions(self, request, *args, **kwargs):
        """List all reply's reactions."""
        reply = self.get_object()
        reactions = reply.replyreaction_set.all()
        data = CommentReactionModelSerializer(reactions, many=True).data
        return Response(data, status=status.HTTP_200_OK)