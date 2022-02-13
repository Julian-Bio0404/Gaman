"""Comments tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Models
from gaman.posts.models import Comment, Post, CommentReaction
from gaman.users.models import FollowUp, User
from rest_framework.authtoken.models import Token


class CommentAPITestCase(APITestCase):
    """Comment api test case."""

    def setUp(self) -> None:
        """Test case setup."""

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

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key
        self.token3 = Token.objects.create(user=self.user3).key

        # User3 follow to user1
        self.folloup = FollowUp.objects.create(
            follower=self.user3, user=self.user1)
        
        self.post = Post.objects.create(
            user=self.user1,
            about='I love Django!!',
            privacy='Private',
            feeling='Curious'
        )

        self.comment = Comment.objects.create(
            author=self.user3,
            post=self.post,
            text='Hi this comment is a test',
            type='Principal-Comment'
        )

    def test_list_post_comments(self):
        """Check that list comments of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('posts:comments-list', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_post_comment(self):
        """Check that list comments of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(
            reverse('posts:comments-detail', args=[self.post.pk, self.comment.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_by_follower(self):
        """
        Check that a follower of the post author can
        comment to the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        request_body = {'text': 'Hi this comment is other test'}
        response = self.client.post(
            reverse('posts:comments-list', args=[self.post.pk]), request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_post_comments_by_follower(self):
        """
        Check that a follower of the post author can
        comment to the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:comments-list', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_post_comment_by_follower(self):
        """
        Check that a follower of the post author can
        see the detail comment.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:comments-detail', args=[self.post.pk, self.comment.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_by_other_user(self):
        """
        Check that a user that is not a follower of
        the post author cannot comment to the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'text': 'Hi this comment is other test'}
        response = self.client.post(
            reverse('posts:comments-list', args=[self.post.pk]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_post_comments_by_other_user(self):
        """
        Check that a user that is not a follower of
        the post author connot list comments of the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(
            reverse('posts:comments-list', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_post_comment_by_other_user(self):
        """
        Check that a user that is not a follower of the post
        author cannot see the detail comment.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(
            reverse('posts:comments-detail', args=[self.post.pk, self.comment.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_react_to_comment(self):
        """Cehck that a user can react to a comment."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        request_body = {'reaction': 'Love'}
        response = self.client.post(
            reverse('posts:comments-react', args=[self.post.pk, self.comment.pk]),
            request_body)
        reaction = CommentReaction.objects.filter(
            user=self.user3, comment=self.comment)
        self.assertEqual(reaction.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_react_to_comment_by_other_user(self):
        """
        Check that a user that is not a follower of the post
        author connot react to a comment of the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'reaction': 'Like'}
        response = self.client.post(
            reverse('posts:comments-react', args=[self.post.pk, self.comment.pk]),
            request_body
        )
        reaction = CommentReaction.objects.filter(
            user=self.user2, comment=self.comment)
        self.assertEqual(reaction.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_comment_replies(self):
        """Check that list replies of a comment is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:comments-replies', args=[self.post.pk, self.comment.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reply_to_comment(self):
        """Check that a user can reply to a comment."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        request_body = {'text': 'This is a test reply'}
        response = self.client.post(
            reverse('posts:comments-reply', args=[self.post.pk, self.comment.pk]),
            request_body
        )
        reply = Comment.objects.filter(
            author=self.user3, post=self.post, type='Reply')
        self.assertEqual(reply.exists(), True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
