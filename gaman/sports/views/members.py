"""Members views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from gaman.sports.permissions import IsClubAdmin, IsSelfMemberOrClubOwner

# Models
from gaman.sports.models import Club
from gaman.sports.models import Invitation, Member

# Serializers
from gaman.sports.serializers import (CreateInvitationSerializer,
                                      ConfirmInvitationSerializer,
                                      InvitationModelSerializer, 
                                      MemberModelSerializer)


class MemberViewSet(viewsets.ModelViewSet):
    """
    Member view set.
    Create, retrieve, expel or deactivate
    a member and list the Club members.
    """

    serializer_class = MemberModelSerializer
    lookup_field = 'user__username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['invitations', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsClubAdmin]
        elif self.action in ['destroy']:
            permissions = [IsAuthenticated, IsSelfMemberOrClubOwner]
        else:
            permissions = [IsAuthenticated]
        return[p() for p in permissions]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the club exists."""
        slugname = kwargs['slugname']
        self.club = get_object_or_404(Club, slugname=slugname)
        return super(MemberViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return club members."""
        members = Member.objects.filter(club=self.club)
        return members
    
    def perform_destroy(self, instance):
        """Delete the member and its invitations."""
        invitation = Invitation.objects.filter(invited=instance.user, club=self.club)
        invitation.delete()
        instance.delete()

    @action(detail=False, methods=['post'])
    def invitations(self, request, *args, **kwargs):
        """Handles the club invitations."""
        serializer = CreateInvitationSerializer(
            data=request.data, context={'issued_by': request.user, 'club': self.club})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Invitation created successfully.'}
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def confirm_invitation(self, request, *args, **kwargs):
        """Handles the invitations confirmation."""
        serializer = ConfirmInvitationSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': f'Now You are a member of {self.club.slugname}'}
        return Response(data, status=status.HTTP_200_OK)