from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Handles user registration with password validation and email uniqueness check.
    Creates a new user with the provided credentials.
    """
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Email is already in use.'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Handles user authentication with email and password.
    Validates credentials and returns user object if successful.
    Returns user object if successful.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email:
            raise serializers.ValidationError({'error': 'Email is required.'})

        if not password:
            raise serializers.ValidationError({'error': 'Password is required.'})

        # Check if user exists and password is correct
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError({'error': 'Invalid credentials.'})
            if not user.is_active:
                raise serializers.ValidationError({'error': 'Account is not active. Please check your email for activation link.'})
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid credentials.'})

        data['user'] = user
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Handles password reset confirmation with new password validation.
    Validates new password and confirmation match.
    """
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if not new_password:
            raise serializers.ValidationError({'error': 'New password is required.'})
        
        if not confirm_password:
            raise serializers.ValidationError({'error': 'Password confirmation is required.'})
        
        if new_password != confirm_password:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        
        return data

