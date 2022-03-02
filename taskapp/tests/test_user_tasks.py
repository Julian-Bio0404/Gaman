"""Users tasks tests"""

# Django
from django.urls import reverse

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Models
from gaman.sponsorships.models import Brand
from gaman.users.models import FollowUp, Profile, User

# Tasks
from taskapp.tasks.users import (send_confirmation_email,
                                 send_restore_password_email,
                                 send_update_email)


class AsynchUserTasksTest(APITestCase):
    """Asynch user task test."""

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

    def test_send_confirmation_email(self):
        """Check that send confirmation email task is success."""
        task = send_confirmation_email.s(user_pk=self.user1.pk).delay()
        self.assertEqual(task.status, 'SUCCESS')

    def test_send_restore_password_email(self):
        """
        Check that send email of restore password
        of the account is success.
        """
        task = send_restore_password_email.s(user_pk=self.user1.pk).delay()
        self.assertEqual(task.status, 'SUCCESS')

    def test_send_update_email(self):
        """Check that send email of update email is success."""
        task = send_update_email.s(
            user_pk=self.user1.pk, email='test@test.com').delay()
        self.assertEqual(task.status, 'SUCCESS')
