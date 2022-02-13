"""Profile tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from gaman.users.models import FollowUp, Profile, User
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

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_profile_detail(self):
        """Verifies that profile detail is success."""
        response = self.client.get(
            reverse('users:profiles-detail', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_profile_update(self):
        """Verifies that the updating of profile is success."""
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

    def test_list_profile_posts(self):
        """Check that list posts of the profile is success."""
        response = self.client.get(
            reverse('users:profiles-posts', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_profile_followers(self):
        """Check that list followers of the profile is success."""
        response = self.client.get(
            reverse('users:profiles-followers', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_profile_following(self):
        """Check that list following of the profile is success."""
        response = self.client.get(
            reverse('users:profiles-following', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_sponsorships(self):
        """Check that list sponsorships of the profile is success."""
        response = self.client.get(
            reverse('users:profiles-sponsorships', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_club_invitations(self):
        """Check that list club-invitations of the user is success."""
        response = self.client.get(
            reverse('users:profiles-invitations', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FollowProfileAPITestCase(APITestCase):
    """Follow profile test."""

    def setUp(self):
        """Test case setup."""
        # Followed
        self.user1 = User.objects.create(
            email='test@gmail.com',
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
            email='test1@gmail.com',
            username='test01',
            first_name='test01',
            last_name='test01',
            role='Athlete',
            password='nKSAJBBCJW_', 
            verified = True
        )
        self.profile2 = Profile.objects.create(user=self.user2)
        self.url = f'http://localhost:8000/profiles/{self.user1.username}/follow/'
        
        # Auth
        self.token = Token.objects.create(user=self.user2).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_follow_success(self):
        """verifies that user1 follows user2 successfully."""
        response = self.client.post(self.url)
        folloup = FollowUp.objects.filter(follower=self.user2, user=self.user1)
        self.assertEqual(folloup.count(), 1)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])