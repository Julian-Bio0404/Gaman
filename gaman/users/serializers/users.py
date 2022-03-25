"""Users serializers."""

# Utilities
import jwt

# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from gaman.users.models import Profile, User

# Serializers
from .profiles import ProfileModelSerializer

# Taskapp
from taskapp.tasks.users import (send_confirmation_email,
                                 send_update_email,
                                 send_restore_password_email)


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'email',
            'phone_number', 'profile',
            'verified', 'role'
        ]

        read_only_fields = [
            'username', 'first_name',
            'last_name', 'email',
            'profile', 'verified'
        ]


class UserSignUpSerializer(serializers.Serializer):
    """
    User signup serializer.
    Handle sign up data validation and user & profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(
        min_length=4, max_length=25,
        validators=[UniqueValidator(queryset=User.objects.all())])

    # Phone number
    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')

    phone_number = serializers.CharField(
        validators=[phone_regex], required=False)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # Role
    def role_validator(rol):
        """Verify the role."""
        if rol not in ['Athlete', 'Sponsor', 'Coach', 'League president']:
            raise serializers.ValidationError('Role not allowed.')

    role = serializers.CharField(
        min_length=4, max_length=16, validators=[role_validator])

    def validate(self, data):
        """Verify password match and type identification."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError('Password don´t match')
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        Profile.objects.create(user=user)
        user_data = UserModelSerializer(user).data
        send_confirmation_email.delay(user_data=user_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.
    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.verified:
            raise serializers.ValidationError('Account is not active yet.')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve token."""
        token, _ = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(
                data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.verified = True
        user.save()


class RefreshTokenSerializer(serializers.Serializer):
    """Refresh Token serializer for account verification."""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials.."""
        user = authenticate(username=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if user.verified == True:
            raise serializers.ValidationError('You are already verified.')
        user_data = UserModelSerializer(user).data
        send_confirmation_email.delay(user_data=user_data)
        return user


class TokenRestorePasswordSerializer(serializers.Serializer):
    """Token restore password serializer."""

    email = serializers.EmailField()

    def validate_email(self, data):
        """Check user's email."""
        try:
            user = User.objects.get(email=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')
        user_data = UserModelSerializer(user).data
        send_restore_password_email.delay(user_data=user_data)
        return user


class RestorePasswordSerializer(serializers.Serializer):
    """Restore user's password serializer."""

    password = serializers.CharField(
        required=True, min_length=8, max_length=64)

    password_confirmation = serializers.CharField(
        required=True, min_length=8, max_length=64)

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(
                data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')

        if payload['type'] != 'restore_password':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        """Restore user's password."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.set_password(self.validated_data['password'])
        user.save()


class UpdatePasswordSerializer(serializers.Serializer):
    """Update user's password serializer."""

    old_password = serializers.CharField(
        required=True, min_length=8, max_length=64)

    password = serializers.CharField(
        required=True, min_length=8, max_length=64)

    password_confirmation = serializers.CharField(
        required=True, min_length=8, max_length=64)

    def validate(self, data):
        """Check password."""
        if not self.context['user'].check_password(data['old_password']):
            raise serializers.ValidationError('Wrong password.')

        if data['password_confirmation'] != data['password']:
            raise serializers.ValidationError('Password don´t match')
        password_validation.validate_password(data['password'])
        return data

    def save(self):
        """Update user's password."""
        user = self.context['user']
        user.set_password(self.validated_data['password'])
        user.save()


class TokenUpdateEmailSerializers(serializers.Serializer):
    """Token Update Email serializer."""

    new_email = serializers.EmailField()

    password = serializers.CharField(
        required=True, min_length=8, max_length=64)

    def validate_new_email(self, data):
        """Check new email address."""
        user = User.objects.filter(email=data)
        if user.exists():
            raise serializers.ValidationError(
                'There is already a user with this email.')
        return data

    def validate(self, data):
        """Check password."""
        user = self.context['user']
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Wrong password.')
        user_data = UserModelSerializer(user).data
        send_update_email.delay(user_data=user_data, email=data['new_email'])
        return data


class UpdateEmailSerializers(serializers.Serializer):
    """Update Email serializer."""

    old_email = serializers.EmailField()
    new_email = serializers.EmailField()
    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(
                data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')

        if payload['type'] != 'update_email':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def validate_old_email(self, data):
        """Check old email address."""
        try:
            user = User.objects.get(email=data)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'There is not user with this email address.')
        self.context['user'] = user
        return data

    def validate(self, data):
        """Check new email address."""
        if data['new_email'] != self.context['payload']['email']:
            raise serializers.ValidationError('This is not you new email address.')
        return data

    def save(self):
        """Update user's email."""
        payload = self.context['payload']
        user = self.context['user']
        user.email = payload['email']
        user.save()
