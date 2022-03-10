"""Member tests."""

# Django REST Framework
from rest_framework.test import APITestCase

# Models
from gaman.sports.models import Club, Invitation
from gaman.users.models import User


class InvitationModelTestCase(APITestCase):
    """Club invitation model test case."""

    def setUp(self) -> None:
        """Test case setup."""
        self.user1 = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Coach',
            password='nKSAJBBCJW_',
            verified=True
        )

        self.user2 = User.objects.create(
            email='test2@gmail.com',
            username='test02',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )

        self.club = Club.objects.create(slugname='Bushido', trainer=self.user1)
        self.invitation = Invitation.objects.create(
            issued_by=self.user1, invited=self.user2, club=self.club)
    
    def test_invitation_model(self):
        """Check that default invitation is not used."""
        self.assertFalse(self.invitation.used)
