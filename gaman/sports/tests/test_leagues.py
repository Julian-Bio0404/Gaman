"""League tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sports.models import League
from gaman.users.models import User


class LeagueGetTetCase(APITestCase):
    """League api test case."""

    def setUp(self) -> None:
        """Test case setup."""

        self.user1 = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key

        self.league1 = League.objects.create(
            country='Colombia',
            state='Huila',
            sport='Karate-Do',
            slugname='Karate-Do Huila'
        )

    def test_list_leagues(self):
        """Check that list leagues is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('sports:leagues-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_league(self):
        """Check that league detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:leagues-detail', args=[self.league1.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
