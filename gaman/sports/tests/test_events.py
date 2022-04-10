"""Sport Events tests."""

# Utilities
import datetime
import json
from unittest import mock

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sports.models import Club, Member, SportEvent
from gaman.sponsorships.models import Brand
from gaman.users.models import User

# Utils
from gaman.utils.data import load_data


class ClubEventsAPITestCase(APITestCase):
    """Club Sport event api test case."""

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

        self.sport_event = SportEvent.objects.create(
            club=self.club,
            title='This is a sport event test',
            start='2022-08-03',
            finish='2022-08-07',
            geolocation='6.26864 -75.55615',
            country='Colombia',
            state='Antioquia',
            city='Medellin',
            place='Atanasio Girardot'
        )

    def test_list_club_events(self):
        """Check that list club events is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:club-events-list', args=[self.club.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_detail(self):
        """Check that sport event detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:club-events-detail',
            args=[self.club.slugname, self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        """Check that sport event delete is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('sports:club-events-detail',
            args=[self.club.slugname, self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_event_by_other_user(self):
        """Check that other user cannot delete the event."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('sports:club-events-detail',
            args=[self.club.slugname, self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event(self):
        """Check that sport event update is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'title': 'This is update test'}
        response = self.client.patch(
            reverse('sports:club-events-detail',
            args=[self.club.slugname, self.sport_event.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_event_by_other_user(self):
        """Check that sport event is fail."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'title': 'This is update test'}
        response = self.client.patch(
            reverse('sports:club-events-detail',
            args=[self.club.slugname, self.sport_event.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventsAPITestCase(APITestCase):
    """Event api test case."""

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

        self.sport_event = SportEvent.objects.create(
            user=self.user1,
            title='This is a sport event test',
            start='2022-08-03',
            finish='2022-08-07',
            geolocation='6.26864 -75.55615',
            country='Colombia',
            state='Antioquia',
            city='Medellin',
            place='Atanasio Girardot'
        )

    def test_list_club_events(self):
        """Check that list club events is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('sports:events-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_detail(self):
        """Check that sport event detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('sports:events-detail', args=[self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        """Check that sport event delete is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('sports:events-detail', args=[self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_by_other_user(self):
        """Check that other user cannot delete the event."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('sports:events-detail', args=[self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @mock.patch('requests.get')
    def test_update_event(self, mock):
        """Check that sport event update is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')

        # Fixture
        geolocation_data = load_data('gaman/sports/tests/fixtures/geolocation.json')
        mock.return_value.json.return_value = geolocation_data

        request_body = {
            'title': 'This is update test',
            'place': '10115 Berlin, Deutschland'
        }
        response = self.client.patch(
            reverse('sports:events-detail', args=[self.sport_event.id]), request_body)
        event = SportEvent.objects.filter(
            user=self.user1, title='This is update test').last()
        self.assertTrue(
            event.title != self.sport_event.title and
            event.geolocation != self.sport_event.geolocation and
            event.country != self.sport_event.country and
            event.state != self.sport_event.state and
            event.city != self.sport_event.city and 
            event.place != self.sport_event.place
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_event_by_other_user(self):
        """Check that sport event is fail."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'title': 'This is update test'}
        response = self.client.patch(
            reverse('sports:events-detail', args=[self.sport_event.id]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_assistants(self):
        """Check that list assistants is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(
            reverse('sports:events-assistants', args=[self.sport_event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_go_to_event(self):
        """Check that go to event is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.post(
            reverse('sports:events-go', args=[self.sport_event.id]))
        self.assertEqual(bool(self.user2 in self.sport_event.assistants.all()), True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @mock.patch('requests.get')
    def test_create_event(self, mock):
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

        response = self.client.post(reverse('sports:events-list'), request_body)
        event = SportEvent.objects.filter(
            title='Event test', description='This is a event test').last()

        self.assertTrue(
            event.geolocation == '52.52896 13.41802' and
            event.country == 'Deutschland' and
            event.state == 'Berlin' and event.city == 'Berlin' and 
            event.place == '10115 Berlin, Deutschland'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_event_failed(self):
        """
        Check that the user cannot create
        a sport event with invalid date.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        today = datetime.date.today()

        # Check start date > finish date
        request_body = {
            'title': 'Event test',
            'description': 'This is a event test',
            'start': today  + datetime.timedelta(days=2),
            'finish': today,
            'place': 'Complejo Acuático Atanasio Girardot, Medellin-Colombia'
        }
        response = self.client.post(reverse('sports:events-list'), request_body)
        error_message = {
            'non_field_errors': ['The start date be must before that finish date.']
        }
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check start date < current date
        request_body['start'] = today  - datetime.timedelta(days=1)
        request_body['finish'] = today + datetime.timedelta(days=2)
        response = self.client.post(reverse('sports:events-list'), request_body)
        error_message = {
            'non_field_errors': ['The dates be must after that current date.']
        }
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check finish date < current date
        request_body['start'] = today
        request_body['finish'] = today - datetime.timedelta(days=1)
        response = self.client.post(reverse('sports:events-list'), request_body)
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EventModelTest(APITestCase):
    """Sport Event model test case."""

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

        self.coach = User.objects.create(
            email='test2@gmail.com',
            username='test02',
            first_name='test00',
            last_name='test00',
            role='Coach',
            password='nKSAJBBCJW_',
            verified=True
        )

        self.sponsor = User.objects.create(
            email='test3@gmail.com',
            username='test03',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_',
            verified=True
        )

        self.club = Club.objects.create(trainer=self.coach, slugname='Bushido')
        self.brand = Brand.objects.create(sponsor=self.sponsor, slugname='SpaceX')

        self.user_event = SportEvent.objects.create(
            user=self.user1,
            title='This is a sport event test',
            start='2022-08-03',
            finish='2022-08-07',
            geolocation='6.26864 -75.55615',
            country='Colombia',
            state='Antioquia',
            city='Medellin',
            place='Atanasio Girardot'
        )

        self.club_event = SportEvent.objects.create(
            club=self.club,
            title='This is a sport event test',
            start='2022-08-03',
            finish='2022-08-07',
            geolocation='6.26864 -75.55615',
            country='Colombia',
            state='Antioquia',
            city='Medellin',
            place='Atanasio Girardot'
        )

        self.brand_event = SportEvent.objects.create(
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

    def test_user_event_model(self):
        """Check that the event author is a user."""
        self.assertEqual(self.user_event.specify_author(), self.user1)
        self.assertEqual(self.user_event.normalize_author(), self.user1)

    def test_club_event_model(self):
        """Check that the event author is a club."""
        self.assertEqual(self.club_event.specify_author(), self.club)
        self.assertEqual(self.club_event.normalize_author(), self.coach)

    def test_brand_event_model(self):
        """Check that the event author is a brand."""
        self.assertEqual(self.brand_event.specify_author(), self.brand)
        self.assertEqual(self.brand_event.normalize_author(), self.sponsor)
