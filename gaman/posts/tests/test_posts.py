"""Posts tests."""

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from gaman.posts.models import Post, PostReaction
from gaman.sponsorships.models import Brand
from gaman.sports.models import Club
from gaman.users.models import FollowUp, User
from rest_framework.authtoken.models import Token


class PostAPITestCase(APITestCase):
    """Post crud test."""

    def setUp(self) -> None:
        """Test case setup."""
        self.url = 'http://localhost:8000/posts/'

        self.user1 = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )

        self.user2 = User.objects.create(
            email='test1@gmail.com',
            username='test01',
            first_name='test01',
            last_name='test01',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )

        # User 1 (coach role)
        self.user3 = User.objects.create(
            email='test3@gmail.com',
            username='test02',
            first_name='test02',
            last_name='test02',
            role='Coach',
            password='nKSAJBBCJW_',
            verified=True
        )

        # A sponsor
        self.user4 = User.objects.create(
            email='test4@gmail.com',
            username='test03',
            first_name='test03',
            last_name='test03',
            role='Sponsor',
            password='nKSAJBBCJW_',
            verified=True
        )

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key
        self.token3 = Token.objects.create(user=self.user3).key
        self.token4 = Token.objects.create(user=self.user4).key

        # User3 follow user1
        self.folloup = FollowUp.objects.create(
            follower=self.user3, user=self.user1)

        self.post = Post.objects.create(
            user=self.user1,
            about='I love Django!!',
            privacy='private',
            feeling='Curious'
        )

        self.brand = Brand.objects.create(sponsor=self.user4, slugname='SpaceX')
        self.club = Club.objects.create(trainer=self.user3, slugname='Bushido')

    def test_creation_user_post(self):
        """Verifies that a user can create a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'about': 'I love Python <3' 
        }
        response = self.client.post(self.url, request_body)
        post = Post.objects.filter(about='I love Python <3')
        self.assertEqual(post.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creation_brand_post(self):
        """Verifies that a brand can create a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token4}')
        url = 'http://localhost:8000/brands/SpaceX/posts/'
        request_body = {
            'about': 'This is a post of SpaceX!'
        }
        response = self.client.post(url, request_body)
        post = Post.objects.filter(brand=self.brand)
        self.assertEqual(post.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creation_club_post(self):
        """Verifies that a club can create a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        url = 'http://localhost:8000/clubs/Bushido/posts/'
        request_body = {
            'about': 'This is a post of SpaceX!'
        }
        response = self.client.post(url, request_body)
        post = Post.objects.filter(club=self.club)
        self.assertEqual(post.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_deletion(self):
        """Verifies that the author can delete a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        url = self.url + f'{self.post.pk}/'
        response = self.client.delete(url)
        post = Post.objects.filter(user=self.user1)
        self.assertEqual(post.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_update_post(self):
        """Verifies that the author can update a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        url = self.url + f'{self.post.pk}/'
        request_body = {
            'about': 'I love Django and FastAPI!!'
        }
        response = self.client.patch(url, request_body)
        post = Post.objects.get(pk=self.post.pk)
        self.assertNotEqual(self.post.about, post.about)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_deletion_by_other_user_fail(self):
        """Verifies that other user cannot delete the post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        url = self.url + f'{self.post.pk}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_updating_by_other_user_fail(self):
        """Verifies that other user cannot update the post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        url = self.url + f'{self.post.pk}/'
        request_body = {
            'about': 'I am a expert in Bioinformatic'
        }
        response = self.client.patch(url, request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_share_post(self):
        """
        Verifies that a follower of the author
        can share the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        url = self.url + f'{self.post.pk}/share/'
        response = self.client.post(url)
        post = Post.objects.filter(post=self.post)
        self.assertEqual(post.exists(), True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_react_to_post(self):
        """
        Verifies that a follower of the author
        can react to the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        url = self.url + f'{self.post.pk}/react/'
        response = self.client.post(url)
        reaction = PostReaction.objects.filter(
            user=self.user3, post=self.post)
        self.assertEqual(reaction.exists(), True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_share_post_by_other_user(self):
        """
        verifies that a user that is not follower of the
        author, cannot share the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        url = self.url + f'{self.post.pk}/share/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_react_post_by_other_user(self):
        """
        Verifies that a user that is not follower of the
        author, cannot react to post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        url = self.url + f'{self.post.pk}/react/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)