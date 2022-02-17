"""Clubs tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sports.models import Club, League
from gaman.users.models import User


class ClubAPITestCase(APITestCase):
    """Club api test case."""

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

        self.league1 = League.objects.create(
            country='Colombia',
            state='Huila',
            sport='Karate-Do',
            slugname='Karate-Do Huila'
        )

        self.club = Club.objects.create(
            league=self.league1,
            slugname='Bushido',
            trainer=self.user1,
            city='Neiva'
        )

    def test_list_clubs(self):
        """Check that list clubs is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('sports:clubs-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_club(self):
        """Check that club detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:clubs-detail', args=[self.club.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_club_followers(self):
        """Check that list club followers is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:clubs-followers', args=[self.club.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_club_sponsorships(self):
        """Check that list club sponsorships is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:clubs-followers', args=[self.club.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_or_unfollow_club(self):
        """Check that follow or unfollow a club is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.post(
            reverse('sports:clubs-follow', args=[self.club.slugname]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(
            reverse('sports:clubs-follow', args=[self.club.slugname]))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_create_club_by_user_without_coach_role(self):
        """Check that the users without coach role, cannot create a club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {
            'league': self.league1.slugname,
            'slugname': 'KaisenDo',
            'city': 'Pitalito'
        }
        response1 = self.client.post(reverse('sports:clubs-list'), request_body)
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response2 = self.client.post(reverse('sports:clubs-list'), request_body)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_club_by_user_with_coach_role(self):
        """Check that the users with coach role, can create a club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'league': self.league1.slugname,
            'slugname': 'Muguiwara',
            'city': 'San Agustín'
        }
        response = self.client.post(reverse('sports:clubs-list'), request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_club_by_creator(self):
        """Check that club creator can update the club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'about':'This is a club test'}
        response = self.client.patch(
            reverse('sports:clubs-detail',
            args=[self.club.slugname]), request_body)
        club = Club.objects.get(trainer=self.user1, slugname='Bushido')
        self.assertNotEqual(self.club.about, club.about)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_club_by_other_user(self):
        """Check that other user cannot update the club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'about':'This is a club test'}
        response = self.client.patch(
            reverse('sports:clubs-detail',
            args=[self.club.slugname]), request_body)
        club = Club.objects.get(trainer=self.user1, slugname='Bushido')
        self.assertEqual(self.club.about, club.about)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_club_by_other_user(self):
        """Check that other user cannot delete the club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('sports:clubs-detail', args=[self.club.slugname]))
        club = Club.objects.filter(trainer=self.user1, slugname='Bushido')
        self.assertTrue(club.exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_club_by_club_creator(self):
        """Check that club creator can delete the club."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('sports:clubs-detail', args=[self.club.slugname]))
        club = Club.objects.filter(trainer=self.user1, slugname='Bushido')
        self.assertFalse(club.exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
