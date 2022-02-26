"""Brand events tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Brand
from gaman.users.models import User


class BrandEventsAPITestCase(APITestCase):
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

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key

        self.brand = Brand.objects.create(
            sponsor=self.user1, slugname='Nike2')
    
    def test_list_brand_events(self):
        """Check that list brand events is succes."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        brand = Brand.objects.get(id=self.brand.id)
        response = self.client.get(
            reverse('sponsorships:brand-events-list', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

