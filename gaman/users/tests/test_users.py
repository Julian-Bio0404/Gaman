"""Users tests."""

# Utilities
import json
from unittest import TestCase

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Models
from gaman.users.models import Profile, User
from rest_framework.authtoken.models import Token

# Serializers
from gaman.users.serializers import UserModelSerializer

# Taskapp
from taskapp.tasks.users import token_generation


class UserSignUpAPITestCase(APITestCase):
    """User sign-up view test."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_'
        )

    def test_password_dont_match(self):
        """
        Verifies that user register is not
        success with password dont match.
        """
        request_body = {
            'email': 'test01@gmail.com',
            'username': 'test01',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': 'Athlete',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW'
        }
        response = self.client.post(reverse('users:users-signup'), request_body)
        error_message = {'non_field_errors': ['Password don´t match']}
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_username_error(self):
        """
        Verifies that the user register is not
        success with username repeat.
        """
        request_body = {
            'email': 'test02@gmail.com',
            'username': self.user.username,
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': 'Athlete',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW'
        }
        response = self.client.post(reverse('users:users-signup'), request_body)
        error_message = {'username': ['This field must be unique.']}
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_email_error(self):
        """
        Verifies that the user register is not
        success with email repeat.
        """
        request_body = {
            'email': self.user.email,
            'username': 'test01',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': 'Athlete',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW'
        }
        response = self.client.post(reverse('users:users-signup'), request_body)
        error_message = {'email': ['This field must be unique.']}
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_role(self):
        """Check that the user register is not success with invalid role."""
        request_body = {
            'email': 'test01@gmail.com',
            'username': 'test01',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': 'xxxxxxx',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW'
        }
        response = self.client.post(reverse('users:users-signup'), request_body)
        error_message = {'role': ['Role not allowed.']}
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_phone_number(self):
        """Check that user register is not success with invalid phone number."""
        request_body = {
            'email': 'test01@gmail.com',
            'username': 'test01',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '9999999999',
            'role': 'Sponsor',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW'
        }
        response = self.client.post(reverse('users:users-signup'), request_body)
        self.assertTrue('phone_number' in json.loads(response.content).keys())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_success(self):
        """
        Verifies that the user sign-up and
        profle creation is success.
        """
        request_body = {
            'email': 'test03@gmail.com',
            'username': 'test01',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': 'Athlete',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW_'
        }
        response = self.client.post(reverse('users:users-signup'), request_body)
        user = User.objects.get(username='test01')
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginAPITestCase(APITestCase):
    """User login view test."""

    def test_login_invalid_credentials(self):
        """Verifies that user login is fail with password incorrect."""
        request_body = {
            'email': 'test2@gmail.com',
            'password': 'nKSAJBu98yBCgfsdg'
        }
        response = self.client.post(reverse('users:users-login'), request_body)
        error_message = {'non_field_errors': ['Invalid credentials.']}
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """Verifies that user login is success."""
        request_body = {
            'email': 'test04@gmail.com',
            'username': 'test04',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': 'Athlete',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW_'
        }
        self.client.post(reverse('users:users-signup'), request_body)

        user = User.objects.get(username='test04')
        user.verified = True
        user.save()

        request_body = {
            'email': user.email,
            'password': 'nKSAJBBCJW_'
        }
        response = self.client.post(reverse('users:users-login'), request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_user_un_verified(self):
        """Verifies that an user un verified can not starts session."""
        request_body = {
            'email': 'test05@gmail.com',
            'username': 'test05',
            'first_name': 'test00',
            'last_name': 'test00',
            'phone_number': '+99 9999999999',
            'role': 'Athlete',
            'password': 'nKSAJBBCJW_',
            'password_confirmation': 'nKSAJBBCJW_'
        }
        self.client.post(reverse('users:users-signup'), request_body)
        user = User.objects.get(username='test05')
        request_body = {
            'email': user.email,
            'password': 'nKSAJBBCJW_'
        }

        error_message = {'non_field_errors': ['Account is not active yet.']}
        response = self.client.post(reverse('users:users-login'), request_body)
        self.assertEqual(json.loads(response.content), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAccountVerifyAPITestCase(APITestCase):
    """User account verify test."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_'
        )

    def test_verify_account_is_false(self):
        """Verifies that account is not verified."""
        self.assertEqual(self.user.verified, False)

    def test_invalid_token(self):
        """Check that verify account is not success with invalid token."""
        request_body = {'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        response = self.client.post(reverse('users:users-verify'), request_body)
        user = User.objects.get(username=self.user.username)
        self.assertFalse(user.verified)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_type_token(self):
        """
        Check that verify account is not success with
        invalid token type.
        """
        user_data = UserModelSerializer(self.user).data
        token = token_generation(user_data=user_data, type='update_email')
        request_body = {'token': token}
        response = self.client.post(reverse('users:users-verify'), request_body)
        user = User.objects.get(username=self.user.username)
        self.assertFalse(user.verified)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_verification(self):
        """Check that the user can refresh token verification."""
        request_body = {'email': self.user.email}
        response = self.client.post(
            reverse('users:users-refresh-token'), request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check with user that does not exist
        request_body['email'] = 'prueba@p.com'
        response = self.client.post(
            reverse('users:users-refresh-token'), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_account(self):
        """Verifies that the account is verified."""
        user_data = UserModelSerializer(self.user).data
        token = token_generation(user_data=user_data, type='email_confirmation')
        request_body = {'token': token}
        response = self.client.post(reverse('users:users-verify'), request_body)
        user = User.objects.get(username=self.user.username)
        self.assertEqual(user.verified, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_psswd_token(self):
        """Check that the user can get token for restore his password."""
        request_body = {'email': self.user.email}
        response = self.client.post(reverse(
            'users:users-token-restore-psswd'), request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check with user that does not exist
        request_body['email'] = 'prueba@p.com'
        response = self.client.post(reverse(
            'users:users-token-restore-psswd'), request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserUpdateAPITestCase(APITestCase):
    """User update test."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            phone_number= '+99 9999999999',
            role='Athlete',
            password='admin123',
            verified=True
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_update_user_phone_number(self):
        """Verifies that the phone number is updated."""
        request_body = {'phone_number': '+99 8888888888'}
        response = self.client.patch(reverse(
            'users:users-detail', args=[self.user.username]), request_body)
        user = User.objects.get(username=self.user.username)
        self.assertNotEqual(self.user.phone_number, user.phone_number)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_email(self):
        """Verifies that update email is success."""
        user_data = UserModelSerializer(self.user).data
        token = token_generation(
            user_data=user_data, type='update_email', email='update@email.com')
        request_body = {
            'old_email': self.user.email,
            'new_email':'update@email.com',
            'token': token
        }
        response = self.client.post(reverse('users:users-update-email'), request_body)
        user = User.objects.get(username=self.user.username)
        self.assertNotEqual(self.user.email, user.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_psswd(self):
    #     """Verifies that update password is success."""
    #     request_body = {
    #         'old_password': 'admin123',
    #         'password': "prueba123",
    #         'password_confirmation': "prueba123"
    #     }
    #     response = self.client.put(
    #         reverse('users:users-update-psswd', args=[self.user.username]), request_body)
    #     user = User.objects.get(username=self.user.username)
    #     self.assertNotEqual(self.user.password, user.password)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_password(self):
        """Verifies that the password is set."""
        # With invalid token
        request_body = {
            'password': 'knjxlksjbda',
            'password_confirmation':'knjxlksjbda',
            'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        }
        response = self.client.post(reverse('users:users-restore-psswd'), request_body)
        user = User.objects.get(username=self.user.username)
        self.assertEqual(self.user.password, user.password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # With invalid token type
        user_data = UserModelSerializer(self.user).data
        token = token_generation(user_data=user_data, type='update_email')
        request_body = {
            'password': 'knjxlksjbda',
            'password_confirmation':'knjxlksjbda',
            'token': token
        }
        response = self.client.post(reverse('users:users-restore-psswd'), request_body)
        self.assertEqual(self.user.password, user.password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Success
        user_data = UserModelSerializer(self.user).data
        token = token_generation(user_data=user_data, type='restore_password')
        request_body = {
            'password': 'knjxlksjbda',
            'password_confirmation':'knjxlksjbda',
            'token': token
        }
        response = self.client.post(reverse('users:users-restore-psswd'), request_body)
        user = User.objects.get(username=self.user.username)
        self.assertNotEqual(self.user.password, user.password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserGetAPITestCase(APITestCase):
    """User detail and list test."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_',
            verified=True
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_user_detail(self):
        """Verifies that user detail exists."""
        response = self.client.get(reverse('users:users-detail', args=[self.user.username]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users(self):
        """Verifies that users list is success."""
        response = self.client.get(reverse('users:users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserModelTestCase(TestCase):
    """User model test case."""

    def setUp(self) -> None:
        """Test case setup."""
        self.user = User.objects.create(
            email='test@gmail.com',
            username='test00',
            first_name='test00',
            last_name='test00',
            role='Athlete',
            password='nKSAJBBCJW_'
        )
    
    def test_user_model(self):
        """Check that attributes and model methods are corrects."""
        self.assertFalse(self.user.verified)
        self.assertFalse(self.user.is_data_completed())

        self.user.phone_number = '+99 9999999999'
        self.user.save()
        self.assertTrue(self.user.is_data_completed())
