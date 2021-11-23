"""Users tests."""

# Django REST Framework
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from gaman.users.models import Profile, User
from rest_framework.authtoken.models import Token

# Taskapp
from taskapp.tasks.users import token_generation


class UserSignUpAPITestCase(APITestCase):
    """User sign-up test."""

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

        self.verified_user = User.objects.create(
            email='test2@gmail.com',
            username='test02',
            first_name='test02',
            last_name='test02',
            role='Athlete',
            password='nKSAJBu98yBCJW_',
            verified=True
        )

        self.url = 'http://localhost:8000/users/signup/'

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
        response = self.client.post(self.url, request_body)
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
        response = self.client.post(self.url, request_body)
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
        response = self.client.post(self.url, request_body)
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
        response = self.client.post(self.url, request_body)
        user = User.objects.get(username='test01')
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        """Verifies that user login is success."""
        url = 'http://localhost:8000/users/login/'
        request_body = {
            'email': self.verified_user.email,
            'password': 'nKSAJBu98yBCJW_'
        }
        response = self.client.post(url, request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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
        self.host = 'http://localhost:8000/'

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_verify_account_is_false(self):
        """Verifies that account is not verified."""
        self.assertEqual(self.user.verified, False)
    
    def test_verify_account(self):
        """Verifies that the account is verified."""
        url = self.host + 'users/verify/'
        token = token_generation(user=self.user, type='email_confirmation')
        request_body = {'token': token}
        self.client.post(url, request_body)
        user = User.objects.get(username=self.user.username)
        self.assertEqual(user.verified, True)

    def test_restore_password(self):
        """Verifies that the password is set."""
        url = self.host + 'users/restore_psswd/'
        token = token_generation(user=self.user, type='restore_password')
        request_body = {
            'password': 'knjxlksjbda',
            'password_confirmation':'knjxlksjbda',
            'token': token
        }
        self.client.post(url, request_body)
        user = User.objects.get(username=self.user.username)
        self.assertNotEqual(self.user.password, user.password)


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
            password='nKSAJBBCJW_',
            verified=True
        )
        self.host = 'http://localhost:8000/'

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_update_user_phone_number(self):
        """Verifies that the phone number is updated."""
        url = self.host +  f'users/{self.user.username}/'
        request_body = {'phone_number': '+99 8888888888'}
        self.client.patch(url, request_body)
        user = User.objects.get(username=self.user.username)
        self.assertNotEqual(self.user.phone_number, user.phone_number)

    def test_update_user_email(self):
        """Verifies that update email is success."""
        token = token_generation(
            user=self.user, type='update_email', email='update@email.com')
        url = self.host + 'users/update_email/'
        request_body = {
            'old_email': self.user.email,
            'new_email':'update@email.com',
            'token': token
        }
        self.client.post(url, request_body)
        user = User.objects.get(username=self.user.username)
        self.assertNotEqual(self.user.email, user.email)


class UserDetailAPITestCase(APITestCase):
    """User detail test."""

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
        self.host = 'http://localhost:8000/'
        self.url = self.host +  f'users/{self.user.username}/'

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_user_detail(self):
        """Verifies that user detail exists."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)