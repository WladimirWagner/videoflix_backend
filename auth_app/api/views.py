from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, CustomTokenObtainPairSerializer, PasswordResetConfirmSerializer
from videoflix_app.models import Profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes

class RegistrationView(APIView):
    """
    Handles user registration endpoint.
    Creates new user and returns user data.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Create Profile for the user
            Profile.objects.create(
                username=user,
                email=user.email
            )
            
            # Generate activation token
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            activation_token = default_token_generator.make_token(user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email
                },
                'token': activation_token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    """
    Handles account activation endpoint.
    Activates user account using uidb64 and token from email.
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid activation link.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if token is valid
        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response(
                    {'message': 'Account successfully activated.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Account is already activated.'},
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'error': 'Invalid or expired activation token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """
    Handles user authentication endpoint.
    Validates credentials and returns user data.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            return Response({
                'detail': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.email,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Handles user logout endpoint.
    Blacklists the refresh token and clears authentication cookies.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token is None:
            return Response(
                {'error': 'Refresh token not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response = Response({
                'detail': 'Logout successful! All tokens will be deleted. Refresh token is now invalid.'
            }, status=status.HTTP_200_OK)
            
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            
            return response
            
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetView(APIView):
    """
    Handles password reset request endpoint.
    Sends password reset email if user with email exists.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_token = default_token_generator.make_token(user)
            
            # TODO: Implement email sending functionality
            # For now, we just return success message
            
            return Response(
                {'detail': 'An email has been sent to reset your password.'},
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {'detail': 'An email has been sent to reset your password.'},
                status=status.HTTP_200_OK
            )


class PasswordResetConfirmView(APIView):
    """
    Handles password reset confirmation endpoint.
    Resets user password using uidb64 and token from email.
    """
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid reset link.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user, token):
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            
            return Response(
                {'detail': 'Your Password has been successfully reset.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid or expired reset token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Handles user authentication endpoint.
    Validates credentials and returns authentication token.
    Sets cookies for refresh and access tokens.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            response = Response({'message': 'Login successful'})

            if access and refresh:
                response.set_cookie(
                    key='access_token', 
                    value=str(access), 
                    httponly=True, 
                    secure=True, 
                    samesite='Lax'
                )
                
                response.set_cookie(
                    key='refresh_token', 
                    value=str(refresh), 
                    httponly=True, 
                    secure=True, 
                    samesite='Lax'
                )

                response.data = {
                    'message': 'Login successful'
                }

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CookieTokenRefreshView(TokenRefreshView):
    """
    Handles token refresh endpoint.
    Refreshes the access token and returns the new access token.
    Sets cookies for refresh and access tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'detail': 'Refresh token not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'refresh': refresh_token})
        if serializer.is_valid():
            access_token = serializer.validated_data['access']
            response = Response({
                'detail': 'Token refreshed',
                'access': access_token
            }, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token', 
                value=access_token, 
                httponly=True, 
                secure=True, 
                samesite='Lax',
                max_age=1800
            )

            return response
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
