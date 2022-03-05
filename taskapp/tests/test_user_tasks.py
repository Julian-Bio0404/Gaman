"""Users tasks tests"""

# Django REST Framework
from rest_framework.test import APITestCase

# Models
from gaman.users.models import User
from gaman.users.models.profiles import Profile

# Serializers
from gaman.users.serializers import UserModelSerializer

# Tasks
from taskapp.tasks.users import (send_confirmation_email,
                                 send_restore_password_email,
                                 send_update_email)


class UserTasksTest(APITestCase):
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

        Profile.objects.create(user=self.user1)
        self.user_data = UserModelSerializer(self.user1).data

    def test_send_confirmation_email(self):
        """Check that send confirmation email task is success."""
        task = send_confirmation_email.s(user_data=self.user_data).delay()
        self.assertEqual(task.get(), 'Success')

    def test_send_restore_password_email(self):
        """
        Check that send email of restore password
        of the account is success.
        """
        task = send_restore_password_email.s(user_data=self.user_data).delay()
        self.assertEqual(task.get(), 'Success')

    def test_send_update_email(self):
        """Check that send email of update email is success."""
        task = send_update_email.s(
            user_data=self.user_data, email='test@test.com').delay()
        self.assertEqual(task.get(), 'Success')
