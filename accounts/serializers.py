from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data representation"""
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user registration with email and password validation"""
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']
    
    def validate_email(self, value):
        """Validate that email is a Gmail address"""
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Only Gmail addresses are allowed')
        return value
    
    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, attrs):
        """Additional validation (if needed)"""
        return super().validate(attrs)
    
    def create(self, validated_data):
        """Create and return a new user instance"""
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with additional validation"""
    def validate(self, attrs):
        email = attrs.get(self.username_field)
        password = attrs.get("password")
        
        # Get user if exists
        user = User.objects.filter(email=email).first()
        
        if not user:
            raise serializers.ValidationError("No account with this email")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is not active")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Wrong password")
        
        # If all checks pass
        data = super().validate(attrs)
        data['user'] = UserSerializer(user).data
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for password reset request"""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Validate that email is a Gmail address"""
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Only Gmail addresses are allowed')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation"""
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value