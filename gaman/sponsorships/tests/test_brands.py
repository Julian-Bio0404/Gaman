"""Brand tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Brand
from gaman.users.models import User


class BrandAPITestCase(APITestCase):
    """Brand api test case."""

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

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key

        self.brand = Brand.objects.create(
            sponsor=self.user1, slugname='Nike')

    def test_list_brands(self):
        """Check that list brands is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('sponsorships:brands-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_brand(self):
        """Check that brand detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse(
            'sponsorships:brands-detail', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_folllowers(self):
        """Check that list followers of a brand is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(reverse(
            'sponsorships:brands-followers', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_brand(self):
        """Check that update brand is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'about': 'This is a brand test',
            'official_web': 'https://www.nike.com/xl/'
        }
        response = self.client.patch(
            reverse('sponsorships:brands-detail',
            args=[self.brand.slugname]), request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_brand(self):
        """Check that update brand is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('sponsorships:brands-detail', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
