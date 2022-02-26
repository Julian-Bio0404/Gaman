"""Brand tests."""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Brand
from gaman.users.models import FollowUp, Profile, User


class BrandAPITestCase(APITestCase):
    """Brand api test case."""

    def setUp(self) -> None:
        """Test case setup."""

        self.user1 = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_',
            phone_number='+99 9999999999',
            verified=True
        )

        self.profile = Profile.objects.create(
            user=self.user1,
            photo='gaman/utils/media_test/profile_photo.jpg',
            cover_photo='gaman/utils/media_test/profile_photo.jpg',
            about='profile test',
            birth_date='1991-08-03',
            country='Colombia',
            web_site='https://www.test.com/',
            social_link='https://www.test.com/'
        )

        self.user2 = User.objects.create(
            email='test2@gmail.com',
            username='test02',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            phone_number='+99 9999999999',
            verified=True
        )

        self.profile2 = Profile.objects.create(
            user=self.user2,
            photo='gaman/utils/media_test/profile_photo.jpg',
            cover_photo='gaman/utils/media_test/profile_photo.jpg',
            about='profile test',
            birth_date='1991-08-03',
            country='Colombia',
            web_site='https://www.test.com/',
            social_link='https://www.test.com/'
        )

        self.user3 = User.objects.create(
            email='test3@gmail.com',
            username='test03',
            first_name='test00',
            last_name='test00',
            role='Sponsor',
            password='nKSAJBBCJW_',
            verified=True
        )

        self.profile3 = Profile.objects.create(
            user=self.user3,
            about='profile test',
            birth_date='1991-08-03',
            country='Colombia',
            web_site='https://www.test.com/',
            social_link='https://www.test.com/'
        )

        # Token for authentication
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key

        self.brand = Brand.objects.create(
            sponsor=self.user1, slugname='Nike')

    def test_list_brands(self):
        """Check that list brands is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse('sponsorships:brands-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_brand(self):
        """Check that brand detail is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.get(reverse(
            'sponsorships:brands-detail', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_folllowers(self):
        """Check that list followers of a brand is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.get(reverse(
            'sponsorships:brands-followers', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_brand(self):
        """Check that update brand is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'about': 'This is a brand test',
            'official_web': 'https://www.nike.com/xl/'
        }
        response = self.client.patch(
            reverse('sponsorships:brands-detail',
            args=[self.brand.slugname]), request_body)
        brand = Brand.objects.get(id=self.brand.id)
        self.assertNotEqual(brand.about, self.brand.about)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brand_by_other_user(self):
        """Check that other user cannot update the brand."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {
            'about': 'This is a brand test',
            'official_web': 'https://www.nike.com/xl/'
        }
        response = self.client.patch(
            reverse('sponsorships:brands-detail',
            args=[self.brand.slugname]), request_body)
        brand = Brand.objects.get(id=self.brand.id)
        self.assertEqual(brand.about, self.brand.about)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_brand(self):
        """Check that update brand is success."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        response = self.client.delete(
            reverse('sponsorships:brands-detail', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_brand_by_other_user(self):
        """Check that other user cannot update the brand."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.delete(
            reverse('sponsorships:brands-detail', args=[self.brand.slugname]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_brand(self):
        """Check that can user can follow a brand."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        response = self.client.post(
            reverse('sponsorships:brands-follow', args=[self.brand.slugname]))
        followup = FollowUp.objects.filter(follower=self.user2, brand=self.brand)
        self.assertTrue(followup.exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_brand(self):
        """Check that user with Sponsor role can create a brand."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
        request_body = {
            'slugname': 'BrandTest',
            'about': 'This is a brand test',
            'official_web': 'https://www.test.com'
        }
        response = self.client.post(reverse('sponsorships:brands-list'), request_body)
        brand = Brand.objects.get(slugname='BrandTest')
        self.assertEqual(brand.sponsor, self.user1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_brand_by_user_without_sponsor_role(self):
        """Check that user without Sponsor role cannot create a brand."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {
            'slugname': 'BrandTest2',
            'about': 'This is a brand test',
            'official_web': 'https://www.test.com'
        }
        response = self.client.post(reverse('sponsorships:brands-list'), request_body)
        brand = Brand.objects.filter(slugname='BrandTest2')
        self.assertFalse(brand.exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_brand_by_user_without_completed_profile(self):
        """
        Check that user with Sponsor role without completed
        profile cannot create a brand.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2}')
        request_body = {
            'slugname': 'BrandTest2',
            'about': 'This is a brand test',
            'official_web': 'https://www.test.com'
        }
        response = self.client.post(reverse('sponsorships:brands-list'), request_body)
        brand = Brand.objects.filter(slugname='BrandTest2')
        self.assertFalse(brand.exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
