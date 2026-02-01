from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User, BlacklistedToken
import jwt
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None  

        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token prefix")
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        if BlacklistedToken.objects.filter(token=token).exists():
            raise AuthenticationFailed("Token has been logged out")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        try:
            user = User.objects.get(id=payload["user_id"], is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, token)