"""Members tests."""

# Django
from urllib import response
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sports.models import Club, Invitation, Member
from gaman.users.models import User


class MembersAPITestCase(APITestCase):
    """Club members api test case."""

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

        self.user3 = User.objects.create(
            email='test3@gmail.com',
            username='test03',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_',
            verified=True
        )

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key
        self.token3 = Token.objects.create(user=self.user3).key

        self.club = Club.objects.create(
            slugname='Bushido',
            trainer=self.user1,
            city='Neiva'
        )

        self.member = Member.objects.create(
            user=self.user2,
            club=self.club,
            active=True
        )

    def test_list_club_members(self):
        """Check that list club members is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:members-list', args=[self.club.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_club_member(self):
        """Check that club member detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:members-detail',
            args=[self.club.slugname, self.user2.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expel_club_member(self):
        """Check that club creator can expel a member of the club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('sports:members-detail',
            args=[self.club.slugname, self.user2.username]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_expel_club_member_by_other_user(self):
        """Check that other user cannot expel a member of the club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.delete(
            reverse('sports:members-detail',
            args=[self.club.slugname, self.user2.username]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_exit_of_club(self):
        """Cehck that a member can exit of the club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('sports:members-detail',
            args=[self.club.slugname, self.user2.username]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_inactive_member(self):
        """Check that the club creator can inactive a member."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'active': False}
        response = self.client.patch(
            reverse('sports:members-detail',
            args=[self.club.slugname, self.user2.username]), request_body)
        member = Member.objects.get(user=self.user2, club=self.club)
        self.assertNotEqual(self.member.active, member.active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inactive_member_fail(self):
        """Check that the member cannot inactive his membership."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'active': False}
        response = self.client.patch(
            reverse('sports:members-detail',
            args=[self.club.slugname, self.user2.username]), request_body)
        member = Member.objects.get(user=self.user2, club=self.club)
        self.assertEqual(self.member.active, member.active)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_invitation(self):
        """Check that the club creator can send an invitation."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'invited': self.user2.username}
        response = self.client.post(
            reverse('sports:members-invitations',
            args=[self.club.slugname]), request_body)
        invitation = Invitation.objects.filter(invited=self.user2)
        self.assertTrue(invitation.exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_confirm_invitation(self):
        """Check that invited user can confirm an invitation."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        invitation = Invitation.objects.create(
            issued_by=self.user1, invited=self.user2, club=self.club)
        request_body = {'id': invitation.id, 'confirm': True}
        response = self.client.post(
            reverse('sports:members-confirm-invitation',
            args=[self.club.slugname]), request_body)
        invitation.refresh_from_db()
        self.assertTrue(invitation.used)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
