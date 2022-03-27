"""Invitation serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from gaman.sports.models import Invitation
from gaman.sports.models.members import Member
from gaman.users.models import User


class InvitationModelSerializer(serializers.ModelSerializer):
    """Invitation model serializer."""

    issued_by = serializers.StringRelatedField(read_only=True)
    invited = serializers.StringRelatedField(read_only=True)
    club = serializers.StringRelatedField(read_only=True)
    used = serializers.BooleanField()

    class Meta:
        """Meta options."""
        model = Invitation
        fields = [
            'id', 'issued_by', 'invited',
            'club', 'used',
            'created'
        ]

        read_only_fields = [
            'issued_by', 'invited',
            'club', 'used', 'created'
        ]


class CreateInvitationSerializer(serializers.Serializer):
    """
    Create Invitation serializer.
    Handle the invitation creation.
    """

    invited = serializers.CharField()

    def validate(self, data):
        """Verify that invited exists."""
        username = data['invited']
        try:
            invited = User.objects.get(username=username)
            self.context['invited'] = invited
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f'The user with username {username} does not exist')

        invitation = Invitation.objects.filter(
            invited=invited, club=self.context['club'])
        if invitation.exists():
            raise serializers.ValidationError(
                'This user already has a invitation for this club.')
        return data

    def create(self, data):
        """Create a invitation."""
        issued_by = self.context['issued_by']
        invited = self.context['invited']
        club = self.context['club']
        invitation = Invitation.objects.create(
            issued_by=issued_by, invited=invited, club=club)

        # Create a inactive Membership
        Member.objects.create(user=invited, club=club)
        return invitation


class ConfirmInvitationSerializer(serializers.Serializer):
    """
    Confirm Invitation serializer.
    Handle the invitation confirmation.
    """
    id = serializers.IntegerField()
    confirm = serializers.BooleanField()

    def validate(self, data):
        """
        Verify that the confirmation is true and that
        the invitations exists.
        """
        try:
            invitation = Invitation.objects.get(id=data['id'])
            self.context['invitation'] = invitation
        except Invitation.DoesNotExist:
            raise serializers.ValidationError(
                'The invitation does not exists.')

        if self.context['user'] != invitation.invited:
            raise serializers.ValidationError(
                'You do not has permissions for this action.')

        if data['confirm'] != True:
            raise serializers.ValidationError(
                'The invitation has not been confirmated.')
        return data

    def save(self):
        """Update the invitation and member."""
        invitation = self.context['invitation']
        invitation.used = True
        invitation.save()

        # Active the member
        member = Member.objects.get(
            user=invitation.invited, club=invitation.club)
        member.active = True
        member.save()
        return invitation
