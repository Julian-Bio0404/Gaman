"""Users views."""

# Django REST framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from gaman.users import serializers

# Models
from gaman.users.models import User

# Serializers
from gaman.users.serializers import (AccountVerificationSerializer,
                                     RefreshTokenSerializer,
                                     RestorePasswordSerializer,
                                     TokenRestorePasswordSerializer,
                                     UpdateEmailSerializers,
                                     UpdatePasswordSerializer,
                                     UserLoginSerializer, UserModelSerializer,
                                     UserSignUpSerializer)
from gaman.users.serializers.users import TokenUpdateEmailSerializers


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    User view set.
    Handle signup, login, account verification, refresh 
    token, update email, restore and update password.
    """

    queryset = User.objects.filter(verified=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data, 'access_token': token}
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations, you can now start using Facebook and connecting with friends.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """Refresh a token verification."""
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We send you an new account verification message to your email.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def token_restore_psswd(self, request):
        """Create a token for restore password."""
        serializer = TokenRestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We have sent an email for you to reset your password.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def restore_psswd(self, request):
        """Restore user's password."""
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your password has been reset.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_psswd(self, request, *args, **kwargs):
        """Update user's password."""
        serializer = UpdatePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def token_update_email(self, request, *args, **kwargs):
        """Create a token for update email address."""
        serializer = TokenUpdateEmailSerializers(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        data = {
            'message': 'We have sent an email for you to update email address.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def update_email(self, request, *args, **kwargs):
        """Update user's email address."""
        serializer = UpdateEmailSerializers(
            data=request.data, 
            context={'user': request.user, 'new_email': request.data['new_email']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Updated email address'}
        return Response(data, status=status.HTTP_200_OK)