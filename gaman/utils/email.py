"""Email utils."""

# Utilities
from datetime import timedelta
import jwt

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


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


def send_email(subject: str, template: tuple, context: dict, email: str):
    """Send a email to user email."""
    from_email = 'Gaman <Gaman.com>'
    content = render_to_string(template, context)
    msg = EmailMultiAlternatives(subject, content, from_email, (email,))
    msg.attach_alternative(content, 'text/html')
    msg.send()
