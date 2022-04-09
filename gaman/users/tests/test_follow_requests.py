"""Follow requests tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Brand
from gaman.sports.models import Club
from gaman.users.models import FollowRequest, FollowUp, Profile, User


class FollowRequestAPITestCase(APITestCase):
    """Follow request test."""

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
            verified=True
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
            verified=True
        )
        self.profile2 = Profile.objects.create(user=self.user2)

        # Other user
        self.user3 = User.objects.create(
            email='test2@gmail.com',
            username='test02',
            first_name='test02',
            last_name='test02',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )
        self.profile3 = Profile.objects.create(user=self.user3)

        # Follow request
        self.follow_request = FollowRequest.objects.create(
            follower=self.user2, followed=self.user1)

        self.url = reverse(
            'users:follow_requests-detail',
            args=[self.user1.username, self.follow_request.pk])

        # Auth
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key
        self.token3 = Token.objects.create(user=self.user3).key
    
    def test_request_model(self):
        """Check that  attributes of request follow model are corrects. """
        self.assertFalse(self.follow_request.accepted)

    def test_confirm_request_for_followed_user(self):
        """
        Verifies that only the followed user,
        can confirms the follow request.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')

        request_body = {'accepted': True}
        response = self.client.put(self.url, request_body)

        follow_request = FollowRequest.objects.get(
            follower=self.user2, followed=self.user1)
        self.assertEqual(follow_request.accepted, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_request_detail(self):
        """Check that follow request detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_requests_list(self):
        """Check that the followed can list his follow requets."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        FollowRequest.objects.create(
            follower=self.user2, followed=self.user1, accepted=True)
        response = self.client.get(
            reverse('users:follow_requests-list', args=[self.user1.username]))
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # By other user
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(
            reverse('users:follow_requests-list', args=[self.user1.username]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_request_for_follower_user(self):
        """
        Verifies that follower user cannot confirm the follow request.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')

        request_body = {'accepted': True}
        response = self.client.put(self.url, request_body)

        follow_request = FollowRequest.objects.get(
            follower=self.user2, followed=self.user1)
        self.assertEqual(follow_request.accepted, False)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_request_for_followed_user(self):
        """Verifies that followed user can delete their follow request."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_request_for_follower_user(self):
        """Verifies that follower user can delete their follow request."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_request_for_other_user(self):
        """Verifies that other user cannot delete the follow request."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FollowModelTestCase(APITestCase):
    """Follow model test case."""

    def setUp(self):
        """Follow up test setup."""
        # Followed
        self.user1 = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )
        Profile.objects.create(user=self.user1)

        # Follower
        self.user2 = User.objects.create(
            email='test1@gmail.com',
            username='test01',
            first_name='test01',
            last_name='test01',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )
        Profile.objects.create(user=self.user2)

        self.brand = Brand.objects.create(sponsor=self.user1, slugname='SpaceX')
        self.club = Club.objects.create(trainer=self.user1, slugname='Bushido')

    def test_follow_model(self):
        """Check that follow model methods are corrects."""
        user_follow = FollowUp.objects.create(follower=self.user2, user=self.user1)
        self.assertEqual(user_follow.specify_followed(), self.user1.username)

        brand_follow = FollowUp.objects.create(follower=self.user2, brand=self.brand)
        self.assertEqual(brand_follow.specify_followed(), self.brand.slugname)

        brand_follow = FollowUp.objects.create(follower=self.user2, club=self.club)
        self.assertEqual(brand_follow.specify_followed(), self.club.slugname)
