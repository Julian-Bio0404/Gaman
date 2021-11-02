"""Follow Request views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.users.permissions import IsFollowedUser, IsFollowerOrFollowed

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

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['retrieve', 'update', 'list']:
           permissions = [IsAuthenticated, IsFollowedUser]
        elif self.action in ['destroy']:
            permissions = [IsFollowerOrFollowed]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exists."""
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(FollowRequestViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return the follow request of user."""
        follow_request = FollowRequest.objects.filter(
            followed=self.user, accepted=False)
        return follow_request

    def update(self, request, *args, **kwargs):
        follow_request = self.get_object()
        serializer = AcceptFollowRequestSerializer(
            data=request.data, context={'follow_request': follow_request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = FollowRequestModelSerializer(follow_request).data
        return Response(data, status=status.HTTP_200_OK)