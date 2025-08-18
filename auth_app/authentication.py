from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that reads token from HTTP-Only cookies.
    Extends the default JWTAuthentication to work with cookies instead of headers.
    """
    
    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication in cookies. Otherwise returns `None`.
        """
        print(f"DEBUG - CookieJWTAuthentication: Checking authentication for {request.path}")
        print(f"DEBUG - Available cookies: {list(request.COOKIES.keys())}")
        
        header = self.get_header(request)
        if header is not None:
            # If Authorization header is present, use standard JWT auth
            print("DEBUG - Found Authorization header")
            raw_token = self.get_raw_token(header)
        else:
            # Try to get token from cookie
            print("DEBUG - No Authorization header, checking cookies")
            raw_token = request.COOKIES.get('access_token')
            print(f"DEBUG - Cookie access_token: {'Found' if raw_token else 'Not found'}")
        
        if raw_token is None:
            print("DEBUG - No token found, authentication failed")
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            print(f"DEBUG - Authentication successful for user: {user.email if user else 'None'}")
            return user, validated_token
        except Exception as e:
            print(f"DEBUG - Token validation failed: {e}")
            return None
    
    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        HTTP header value, or from cookies.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty header or cookie value
            return None

        if len(parts) == 1:
            # Assume cookie value (just the token)
            return parts[0]

        if len(parts) == 2 and parts[0].lower() == 'bearer':
            # Standard Authorization: Bearer <token>
            return parts[1]

        return None
