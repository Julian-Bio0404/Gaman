"""Utils Functions."""

# Utilities
import jwt
from datetime import timedelta

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Models
from gaman.users.models import User


def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    user = User.objects.get(pk=user_pk)
    type = 'email_confirmation'
    token = token_generation(user, type)
    subject = 'Welcome @{}! Verify your account'.format(user.get_full_name())
    from_email = 'Gaman <Gaman.com>'
    content = render_to_string(
        'users/account_verification.html', {'token': token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()


def send_restore_password_email(user_pk):
    """Send restore password link to given user."""
    user = User.objects.get(pk=user_pk)
    type = 'restore_password'
    token = token_generation(user, type)
    subject = 'Update your password'
    from_email = 'Gaman <Gaman.com>'
    content = render_to_string(
        'users/restore_password.html', {'token': token, 'user': user})
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, 'text/html')
    msg.send()


def token_generation(user, type):
    """Create JWT token."""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': type}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
