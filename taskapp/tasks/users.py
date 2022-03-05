"""Users tasks."""

from __future__ import absolute_import, unicode_literals

# Utilities
from datetime import timedelta
import jwt

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Celery
from taskapp.celery import app


def token_generation(user_data: dict, type: str, email=None) -> str:
    """Create JWT token."""
    exp_date = timezone.now() + timedelta(days=2)
    if type in ['email_confirmation', 'restore_password']:
        payload = {
            'user': user_data['username'],
            'exp': int(exp_date.timestamp()),
            'type': type}
    elif type in ['update_email']:
        payload = {
            'email': email,
            'exp': int(exp_date.timestamp()),
            'type': type}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


# Asynch task
@app.task(bind=True)
def send_confirmation_email(self, user_data: dict):
    """Send account verification link to given user."""
    type = 'email_confirmation'
    token = token_generation(user_data, type)
    subject = 'Welcome @{}! Verify your account'.format(user_data['username'])
    from_email = 'Gaman <Gaman.com>'
    content = render_to_string(
        'users/account_verification.html',
        {'token': token, 'user': user_data['username']})
    msg = EmailMultiAlternatives(subject, content, from_email, [user_data['email']])
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return 'Success'


# Asynch task
@app.task(bind=True)
def send_restore_password_email(self, user_data: dict):
    """Send restore password link to given user."""
    type = 'restore_password'
    token = token_generation(user_data, type)
    subject = 'Update your password'
    from_email = 'Gaman <Gaman.com>'
    content = render_to_string(
        'users/restore_password.html',
        {'token': token, 'user': user_data['username']})
    msg = EmailMultiAlternatives(subject, content, from_email, [user_data['email']])
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return 'Success'


# Asynch task
@app.task(bind=True)
def send_update_email(self, user_data: dict, email: str):
    """Send update email link to given user."""
    type = 'update_email'
    token = token_generation(user_data, type, email)
    subject = 'Hi @{}! Update your email'.format(user_data['username'])
    from_email = 'Gaman <Gaman.com>'
    content = render_to_string(
        'users/update_email.html', {'token': token, 'user': user_data['username']})
    msg = EmailMultiAlternatives(subject, content, from_email, [email])
    msg.attach_alternative(content, 'text/html')
    msg.send()
    return 'Success'
