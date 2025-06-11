from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    UserCreateSerializer,
    CustomTokenObtainPairSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class UserCreateView(generics.CreateAPIView):
    """Handle user registration."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'User created successfully'},
            status=status.HTTP_201_CREATED
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Handle user login with JWT token generation."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    """Handle user logout."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK
        )


class PasswordResetRequestView(generics.GenericAPIView):
    """Handle password reset request by sending a reset link."""
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request).domain
            relative_link = reverse(
                'password-reset-confirm',
                kwargs={'uidb64': uidb64, 'token': token}
            )
            abs_url = f'http://{current_site}{relative_link}'

            email_body = f'Hello,\nUse the link below to reset your password:\n{abs_url}'
            send_mail(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        return Response(
            {'success': 'We have sent you a link to reset your password'},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """Handle password reset confirmation and password update."""
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    'success': True,
                    'message': 'Credentials are valid',
                },
                status=status.HTTP_200_OK
            )

        except DjangoUnicodeDecodeError:
            return Response(
                {'error': 'Token is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data['password'])
            user.save()

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'success': 'Password reset successfully',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserCreateSerializer(user).data
                },
                status=status.HTTP_200_OK
            )

        except DjangoUnicodeDecodeError:
            return Response(
                {'error': 'Token is not valid'},
                status=status.HTTP_400_BAD_REQUEST
            )