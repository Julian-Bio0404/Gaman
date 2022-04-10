"""Brand events tests."""

# Utilities
import datetime
from unittest import mock

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Brand
from gaman.sports.models import SportEvent
from gaman.users.models import User

# Utils
from gaman.utils.data import load_data

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

        self.user2 = User.objects.create(
            email='test2@gmail.com',
            username='test02',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            phone_number='+99 9999999999',
            verified=True
        )

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key

        self.brand = Brand.objects.create(
            sponsor=self.user1, slugname='Nike2')
        
        self.sport_event = SportEvent.objects.create(
            brand=self.brand,
            title='This is a sport event test',
            start='2022-08-03',
            finish='2022-08-07',
            geolocation='6.26864 -75.55615',
            country='Colombia',
            state='Antioquia',
            city='Medellin',
            place='Atanasio Girardot'
        )
    
    def test_list_brand_events(self):
        """Check that list brand events is succes."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sponsorships:brand-events-list', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_brand_event(self):
        """Check that brand event detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sponsorships:brand-events-detail',
            args=[self.brand.slugname, self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_brand_event(self):
        """Check that update brand event is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'start':'2022-08-04',
            'finish': '2022-08-08',
        }
        response = self.client.patch(
            reverse('sponsorships:brand-events-detail',
            args=[self.brand.slugname, self.sport_event.id]), request_body)
        event = SportEvent.objects.get(id=self.sport_event.id)
        self.assertNotEqual(event.start, self.sport_event.start)
        self.assertNotEqual(event.finish, self.sport_event.finish)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_brand_event_by_other_user(self):
        """Check that other user cannot update the event."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {
            'start':'2022-08-04',
            'finish': '2022-08-08',
        }
        response = self.client.patch(
            reverse('sponsorships:brand-events-detail',
            args=[self.brand.slugname, self.sport_event.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_brand_event(self):
        """Check that delete brand event is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('sponsorships:brand-events-detail',
            args=[self.brand.slugname, self.sport_event.id]))
        event = SportEvent.objects.filter(id=self.sport_event.id)
        self.assertEqual(event.exists(), False)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_brand_event_by_other_user(self):
        """Check that other user connot delete brand event."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('sponsorships:brand-events-detail',
            args=[self.brand.slugname, self.sport_event.id]))
        event = SportEvent.objects.filter(id=self.sport_event.id)
        self.assertEqual(event.exists(), True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch('requests.get')
    def test_create_brand_event(self, mock):
        """Check that the user can create a sport event."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')

        # Fixture
        geolocation_data = load_data('gaman/sports/tests/fixtures/geolocation.json')
        mock.return_value.json.return_value = geolocation_data

        today = datetime.date.today()
        request_body = {
            'title': 'Event test',
            'description': 'This is a event test',
            'start': today,
            'finish': today  + datetime.timedelta(days=2),
            'place': 'Complejo Acuático Atanasio Girardot, Medellin-Colombia'
        }

        response = self.client.post(
            reverse('sponsorships:brand-events-list',
            args=[self.brand.slugname]), request_body)
        event = SportEvent.objects.filter(
            title='Event test', description='This is a event test').last()

        self.assertTrue(
            event.geolocation == '52.52896 13.41802' and
            event.country == 'Deutschland' and
            event.state == 'Berlin' and event.city == 'Berlin' and 
            event.place == '10115 Berlin, Deutschland'
        )
        self.assertEqual(event.brand, self.brand)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
