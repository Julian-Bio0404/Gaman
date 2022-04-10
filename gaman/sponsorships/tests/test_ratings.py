"""Ratings tests."""

# Utilities
import datetime

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Sponsorship, Rating
from gaman.users.models import User


class RatingsAPITestCase(APITestCase):
    """Brand api test case."""

    def setUp(self) -> None:
        """Test case setup."""

        self.user1 = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_',
            phone_number='+99 9999999999',
            verified=True
        )

        self.sponsor = User.objects.create(
            email='test2@gmail.com',
            username='test02',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_',
            phone_number='+99 9999999999',
            verified=True
        )

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.sponsor).key

        self.sponsorship = Sponsorship.objects.create(
            sponsor=self.sponsor,
            athlete=self.user1,
            start=datetime.date.today(),
            finish=datetime.date.today() + datetime.timedelta(days=2)
        )

        self.rating = Rating.objects.create(
            sponsorship=self.sponsorship,
            qualifier=self.user1,
            comment='This is a sponsorship rating test.',
            rating=9.8
        )

    def test_rating_list(self):
        """Check that rating list is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sponsorships:ratings-list', args=[self.sponsorship.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rating_detail(self):
        """Check that rating detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sponsorships:ratings-detail',
            args=[self.sponsorship.id, self.rating.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_rating(self):
        """Check that the user can create a rating."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')

        # Check rating already exist
        request_body = {
            'comment': 'This is a sponsorship rating test.',
            'rating': 9.2
        }
        response = self.client.post(
            reverse('sponsorships:ratings-list',
            args=[self.sponsorship.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check comment must be greater than 30 characters
        request_body = {
            'comment': 'This is a rating.',
            'rating': 9.2
        }
        response = self.client.post(
            reverse('sponsorships:ratings-list',
            args=[self.sponsorship.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Success
        Rating.objects.all().delete()
        request_body = {
            'comment': 'This is a sponsorship rating test.',
            'rating': 9.2
        }
        response = self.client.post(
            reverse('sponsorships:ratings-list',
            args=[self.sponsorship.id]), request_body)
        self.assertTrue(Rating.objects.filter(id=2).exists)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_rating_by_other_user(self):
        """Check that other user cannot create a rating."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {
            'comment': 'This is a sponsorship rating test.',
            'rating': 9.2
        }
        response = self.client.post(
            reverse('sponsorships:ratings-list',
            args=[self.sponsorship.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_rating(self):
        """Check that the only qualifier can update his rating."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'rating': 9.5}
        response = self.client.patch(
            reverse('sponsorships:ratings-detail',
            args=[self.sponsorship.id, self.rating.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # By other user
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'rating': 9.9}
        response = self.client.patch(
            reverse('sponsorships:ratings-detail',
            args=[self.sponsorship.id, self.rating.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
