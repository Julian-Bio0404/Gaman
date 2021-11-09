"""Posts tests."""

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from gaman.users.models import FollowUp, User
from gaman.posts.models import Post, PostReaction
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

        # Follower of the user 1
        self.user3 = User.objects.create(
            email='test3@gmail.com',
            username='test02',
            first_name='test02',
            last_name='test02',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )

        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key
        self.token3 = Token.objects.create(user=self.user3).key

        self.folloup = FollowUp.objects.create(
            follower=self.user3, user=self.user1)

        self.post = Post.objects.create(
            author=self.user1,
            about='I love Django!!',
            privacy='private',
            feeling='Curious'
        )

    def test_post_creation(self):
        """Verifies that a user can create a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'about': 'I love Python <3' 
        }
        response = self.client.post(self.url, request_body)
        post = Post.objects.filter(author=self.user1, pk=2)
        self.assertEqual(post.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_post_deletion(self):
        """Verifies that the author can delete a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        url = self.url + f'{self.post.pk}/'
        response = self.client.delete(url)
        post = Post.objects.filter(author=self.user1)
        self.assertEqual(post.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_update_post(self):
        """Verifies that the author can update a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        url = self.url + f'{self.post.pk}/'
        reques_body = {
            'about': 'I love Django and FastAPI!!'
        }
        response = self.client.patch(url, reques_body)
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
        self.assertEqual(reaction.exists, True)
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