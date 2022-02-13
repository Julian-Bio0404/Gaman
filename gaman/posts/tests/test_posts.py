"""Posts tests."""

# Django
from django.urls import reverse

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

        # User3 follow to user1
        self.folloup = FollowUp.objects.create(
            follower=self.user3, user=self.user1)

        self.post = Post.objects.create(
            user=self.user1,
            about='I love Django!!',
            privacy='Private',
            feeling='Curious'
        )

        self.brand = Brand.objects.create(sponsor=self.user4, slugname='SpaceX')
        self.club = Club.objects.create(trainer=self.user3, slugname='Bushido')

    def test_list_posts(self):
        """Check that list posts is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('posts:posts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail(self):
        """Check that post detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('posts:posts-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_user_post(self):
        """Verifies that a user can create a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'about': 'I love Python <3'}
        response = self.client.post(reverse('posts:posts-list'), request_body)
        post = Post.objects.filter(about='I love Python <3')
        self.assertEqual(post.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creation_brand_post(self):
        """Verifies that a brand can create a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token4}')
        request_body = {'about': 'This is a post of SpaceX!'}
        response = self.client.post(reverse(
            'sponsorships:brand-posts-list', args=[self.brand.slugname]), request_body)
        post = Post.objects.filter(brand=self.brand)
        self.assertEqual(post.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creation_club_post(self):
        """Verifies that a club can create a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        request_body = {'about': 'This is a post of SpaceX!'}
        response = self.client.post(reverse(
            'sports:club-posts-list', args=[self.club.slugname]), request_body)
        post = Post.objects.filter(club=self.club)
        self.assertEqual(post.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        """Verifies that the author can update a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {'about': 'I love Django and FastAPI!!'}
        response = self.client.patch(reverse(
            'posts:posts-detail', args=[self.post.pk]), request_body)
        post = Post.objects.get(pk=self.post.pk)
        self.assertNotEqual(self.post.about, post.about)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_deletion(self):
        """Verifies that the author can delete a post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('posts:posts-detail', args=[self.post.pk]))
        post = Post.objects.filter(user=self.user1)
        self.assertEqual(post.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_deletion_by_other_user_fail(self):
        """Verifies that other user cannot delete the post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('posts:posts-detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_updating_by_other_user_fail(self):
        """Verifies that other user cannot update the post."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'about': 'I am a expert in Bioinformatic'}
        response = self.client.patch(reverse(
            'posts:posts-detail', args=[self.post.pk]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_share_post(self):
        """
        Verifies that a follower of the author
        can share the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.post(
            reverse('posts:posts-share', args=[self.post.pk]))
        post = Post.objects.filter(post=self.post)
        self.assertEqual(post.exists(), True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_react_to_post(self):
        """
        Verifies that a follower of the author
        can react to the post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        request_body = {'reaction': 'Like'}
        response = self.client.post(
            reverse('posts:posts-react', args=[self.post.pk]), request_body)
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
        response = self.client.post(
            reverse('posts:posts-react', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_react_post_by_other_user(self):
        """
        Verifies that a user that is not follower of the
        author, cannot react to post.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {'reaction': 'Like'}
        response = self.client.post(
            reverse('posts:posts-react', args=[self.post.pk]), request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_post_reactions(self):
        """Check that list reactions of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:posts-reactions', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_likes(self):
        """Check that list likes of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:posts-likes', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_loves(self):
        """Check that list loves reactions of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:posts-loves', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_hahas(self):
        """Check that list hahas reactions of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:posts-hahas', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_curious(self):
        """Check that list curious reactions of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:posts-curious', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_angry(self):
        """Check that list angry reactions of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:posts-angry', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_sads(self):
        """Check that list sad reactions of a post is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token3}')
        response = self.client.get(
            reverse('posts:posts-sads', args=[self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
