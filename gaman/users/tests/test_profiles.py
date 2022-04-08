"""Profile tests."""

# Utilities
import datetime
import json

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from gaman.sports.models import Invitation, Club
from gaman.sponsorships.models import Sponsorship
from gaman.users.models import FollowRequest, FollowUp, Profile, User
from rest_framework.authtoken.models import Token


class ProfileAPITestCase(APITestCase):
    """Profile API test."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_', 
            verified = True
        )
        Profile.objects.create(user=self.user)

        self.user2 = User.objects.create(
            email='test0@gmail.com',
            username='test000',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_', 
            verified = True
        )
        Profile.objects.create(user=self.user2)

        self.sponsor = User.objects.create(
            email='test1@gmail.com',
            username='test01',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_', 
            verified = True
        )
        Profile.objects.create(user=self.sponsor)

        # Follow up
        FollowUp.objects.create(user=self.user, follower=self.user2)
        FollowUp.objects.create(user=self.user2, follower=self.user)

        # Club
        self.club = Club.objects.create(slugname='Bushido', trainer=self.user2)

        # Invitation
        self.invitation = Invitation.objects.create(
            club=self.club, issued_by=self.sponsor, invited=self.user)

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.token2 = Token.objects.create(user=self.sponsor).key

    def test_profile_detail(self):
        """Verifies that profile detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(
            reverse('users:profiles-detail', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(
            reverse('users:profiles-detail', args=[self.sponsor.username]))
        self.assertTrue('rating' in json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update(self):
        """Verifies that the updating of profile is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        request_body = {
            'about': 'I am a test profile',
            'birth_date': '1997-09-24',
            'sport': 'Karate',
            'country': 'Colombia',
            'public': False,
            'web_site': 'https://github.com/',
            'social_link': 'https://github.com/'
        }
        response = self.client.patch(reverse(
            'users:profiles-detail', args=[self.user.username]), request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_update_by_other_user(self):
        """Check that other user cannot update profile."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {
            'about': 'I am a test profile',
            'birth_date': '1997-09-24',
            'sport': 'Karate',
            'country': 'Colombia',
            'public': False,
            'web_site': 'https://github.com/',
            'social_link': 'https://github.com/'
        }
        response = self.client.patch(reverse(
            'users:profiles-detail', args=[self.user.username]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_profile_posts(self):
        """Check that list posts of the profile is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(
            reverse('users:profiles-posts', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(
            reverse('users:profiles-posts', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_profile_followers(self):
        """Check that list followers of the profile is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(
            reverse('users:profiles-followers', args=[self.user.username]))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_profile_following(self):
        """Check that list following of the profile is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(
            reverse('users:profiles-following', args=[self.user.username]))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_sponsorships(self):
        """Check that list sponsorships of the profile is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Sponsorship
        today = datetime.date.today()
        start = today
        finish = today + datetime.timedelta(days=2)
        Sponsorship.objects.create(
            sponsor=self.sponsor, athlete=self.user, start=start, finish=finish)

        response = self.client.get(
            reverse('users:profiles-sponsorships', args=[self.user.username]))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_club_invitations(self):
        """Check that list club-invitations of the user is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(
            reverse('users:profiles-invitations', args=[self.user.username]))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FollowProfileAPITestCase(APITestCase):
    """Follow profile test."""

    def setUp(self):
        """Test case setup."""
        # Followed
        self.user1 = User.objects.create(
            email='user1@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_', 
            verified = True
        )
        self.profile1 = Profile.objects.create(user=self.user1)

        # Follower
        self.user2 = User.objects.create(
            email='user2@gmail.com',
            username='test01',
            first_name='test01',
            last_name='test01',
            role='Athlete',
            password='nKSAJBBCJW_', 
            verified = True
        )
        self.profile2 = Profile.objects.create(user=self.user2)

        self.user3 = User.objects.create(
            email='user3@gmail.com',
            username='test02',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_', 
            verified = True
        )
        # Private Profile
        self.profile3 = Profile.objects.create(user=self.user3, public=False)

        # Auth
        self.token = Token.objects.create(user=self.user2).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_follow_public_profile(self):
        """verifies that user2 follows to user1 successfully."""
        response = self.client.post(reverse(
            'users:profiles-follow', args=[self.user1.username]))
        folloup = FollowUp.objects.filter(follower=self.user2, user=self.user1)
        self.assertEqual(folloup.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_private_profile(self):
        """Verifies that user2 follows to user3 with private profile."""
        response = self.client.post(reverse(
            'users:profiles-follow', args=[self.user3.username]))
        folloup = FollowUp.objects.filter(follower=self.user2, user=self.user1)
        follow_request = FollowRequest.objects.filter(
            follower=self.user2, followed=self.user3)
        self.assertEqual(folloup.count(), 0)
        self.assertEqual(follow_request.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileModelTestCase(APITestCase):
    """Profile model test case."""

    def setUp(self) -> None:
        """Test case setup."""
        self.user1 = User.objects.create(
            email='user1@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_', 
            verified = True
        )

        self.profile1 = Profile.objects.create(user=self.user1)
    
    def test_profile_model(self):
        """Check that attributes and model methods are corrects."""
        self.assertTrue(self.profile1.public)
        self.assertFalse(self.profile1.is_data_completed())

        self.profile1.photo = 'gaman/utils/media_test/profile_photo.jpg'
        self.profile1.cover_photo = 'gaman/utils/media_test/profile_photo.jpg'
        self.profile1.about = 'I am a profile test'
        self.profile1.birth_date = '1997-04-04'
        self.profile1.country = 'Colombia'
        self.profile1.web_site = 'www.xxxxxx.com'
        self.profile1.social_link = 'www.xxxxxx.com'
        self.profile1.save()

        self.assertTrue(self.profile1.is_data_completed())
