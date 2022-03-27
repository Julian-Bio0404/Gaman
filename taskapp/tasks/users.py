"""Users tasks."""

from __future__ import absolute_import, unicode_literals

# Utils
from gaman.utils.email import send_email, token_generation

# Celery
from taskapp.celery import app


# Asynch task
@app.task(bind=True)
def send_confirmation_email(self, user_data: dict):
    """Send account verification link to given user."""
    token = token_generation(user_data, type='email_confirmation')
    email_data = {
        'subject': f"Welcome @{user_data['username']}! Verify your account",
        'template': 'users/account_verification.html',
        'context': {'token': token, 'user': user_data['username']},
        'email': user_data['email']
    }
    send_email(**email_data)
    return 'Success'


# Asynch task
@app.task(bind=True)
def send_restore_password_email(self, user_data: dict):
    """Send restore password link to given user."""
    token = token_generation(user_data, type='restore_password')
    email_data = {
        'subject': 'Update your password',
        'template': 'users/restore_password.html',
        'context': {'token': token, 'user': user_data['username']},
        'email': user_data['email']
    }
    send_email(**email_data)
    return 'Success'


# Asynch task
@app.task(bind=True)
def send_update_email(self, user_data: dict, email: str):
    """Send update email link to given user."""
    token = token_generation(user_data, type='update_email', email=email)
    email_data = {
        'subject': f"Hi @{user_data['username']}! Update your email",
        'template': 'users/update_email.html',
        'context': {'token': token, 'user': user_data['username']},
        'email': user_data['email']
    }
    send_email(**email_data)
    return 'Success'
