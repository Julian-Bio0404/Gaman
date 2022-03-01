"""Sport Events tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sports.models import Club, Member, SportEvent
from gaman.users.models import User


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

    def test_update_event(self):
        """Check that sport event update is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'title': 'This is update test'}
        response = self.client.patch(
            reverse('sports:events-detail', args=[self.sport_event.id]), request_body)
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
