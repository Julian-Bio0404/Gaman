"""Friend requests views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Models
from gaman.users.models import FollowRequest, User

# Serializers
from gaman.users.serializers import (AcceptFollowRequestSerializer,
                                     FollowRequestModelSerializer)


class FollowRequestViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """
    Follow request viewset.
    Handle the acceptance and list of follow requests.
    """

    serializer_class = FollowRequestModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(FollowRequestViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return the follow request of user."""
        follow_request = FollowRequest.objects.filter(
            followed=self.user)
        return follow_request

    def list(self, request, *args, **kwargs):
        """List all user's friend request."""
        if request.user == self.user:
            follow_requests = FollowRequest.objects.filter(
                followed=request.user, accepted=False)
            data = FollowRequestModelSerializer(follow_requests, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'You do not have permission for this action.'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        follow_request = self.get_object()
        serializer = AcceptFollowRequestSerializer(
            data=request.data, context={'follow_request': follow_request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = FollowRequestModelSerializer(follow_request).data
        return Response(data, status=status.HTTP_200_OK)