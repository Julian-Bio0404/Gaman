"""Sponsorship tests."""

# Utilities
import datetime

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Brand, Sponsorship
from gaman.users.models import Profile, User


class SponsorshipTestCase(APITestCase):
    """Sponsorship api test case."""

    def setUp(self) -> None:
        """Test case setup."""

        self.sponsor = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_',
            phone_number='+99 9999999999',
            verified=True
        )

        Profile.objects.create(
            user=self.sponsor,
            photo='gaman/utils/media_test/profile_photo.jpg',
            cover_photo='gaman/utils/media_test/profile_photo.jpg',
            about='profile test',
            birth_date='1990-08-03',
            country='Colombia',
            web_site='https://www.test.com/',
            social_link='https://www.test.com/'
        )

        self.athlete = User.objects.create(
            email='test1@gmail.com',
            username='test01',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            phone_number='+99 9999999999',
            verified=True
        )

        Profile.objects.create(
            user=self.athlete,
            photo='gaman/utils/media_test/profile_photo.jpg',
            cover_photo='gaman/utils/media_test/profile_photo.jpg',
            about='profile test',
            birth_date='1999-08-03',
            country='Colombia',
            web_site='https://www.test.com/',
            social_link='https://www.test.com/'
        )

        # Token for authentication
        self.token1 = Token.objects.create(user=self.sponsor).key
        self.token2 = Token.objects.create(user=self.athlete).key

        self.brand = Brand.objects.create(
            sponsor=self.sponsor, slugname='Nike')
    
    def test_create_sponsorship(self):
        """Check that sponsorship creation by sponsor is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'brand': self.brand.slugname,
            'athlete': self.athlete.username,
            'start': '2022-12-01',
            'finish': '2023-12-01'
        }
        response = self.client.post(
            reverse('sponsorships:sponsorships-list'), request_body)
        sponsorship = Sponsorship.objects.filter(
            sponsor=self.sponsor,athlete=self.athlete)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(sponsorship.exists())

        # Check with athlete username non-existent
        request_body = {
            'brand': self.brand.slugname,
            'athlete': 'xxxxxxxxxx',
            'start': '2022-12-01',
            'finish': '2023-12-01'
        }
        response = self.client.post(
            reverse('sponsorships:sponsorships-list'), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check with brand slugname non-existent
        request_body = {
            'brand': 'xxxxxxxxxx',
            'athlete': self.athlete.username,
            'start': '2022-12-01',
            'finish': '2023-12-01'
        }
        response = self.client.post(
            reverse('sponsorships:sponsorships-list'), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check with start date < current date
        request_body = {
            'brand': self.brand.slugname,
            'athlete': self.athlete.username,
            'start': '1999-12-01',
            'finish': '2023-12-01'
        }
        response = self.client.post(
            reverse('sponsorships:sponsorships-list'), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check with finish date < current date
        request_body = {
            'brand': self.brand.slugname,
            'athlete': self.athlete.username,
            'start': '2023-12-01',
            'finish': '1999-12-01'
        }
        response = self.client.post(
            reverse('sponsorships:sponsorships-list'), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check with start date > finish date
        request_body = {
            'brand': self.brand.slugname,
            'athlete': self.athlete.username,
            'start': datetime.date.today() + datetime.timedelta(days=2),
            'finish': datetime.date.today()
        }
        response = self.client.post(
            reverse('sponsorships:sponsorships-list'), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sponsorship_detail(self):
        """Check that sponsorship detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        today = datetime.date.today()
        start = today
        finish = today + datetime.timedelta(days=2)
        sponsorship = Sponsorship.objects.create(
            sponsor=self.sponsor,
            athlete=self.athlete, start=start, finish=finish
        )
        response = self.client.get(
            reverse('sponsorships:sponsorships-detail', args=[sponsorship.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
