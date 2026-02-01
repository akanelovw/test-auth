from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .permissions.permissions import PERMISSIONS

from .permissions.decorators import is_admin, permission_check
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UpdateUserSerializer
from .models import User, BlacklistedToken
from .authentication import JWTAuthentication
from .services.jwt import generate_jwt


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # сохраняем пользователя

        return Response({
            "message": "User registered",
            "id": str(user.id)
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = generate_jwt(user)
        return Response({"token": token}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    
    @permission_check("user_account", "delete")
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @permission_check("user_account", "delete")
    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @permission_check("user_account", "delete")
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = False
        user.save()
        
        return Response({"message": "User deactivated"}, status=status.HTTP_204_NO_CONTENT)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        token = request.auth
        BlacklistedToken.objects.create(token=token)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    
    
class PermissionConfigView(APIView):
    authentication_classes = [JWTAuthentication]

    @is_admin
    def get(self, request):
        return Response(PERMISSIONS)

    @is_admin
    def patch(self, request):
        """
        {
          "role": "user",
          "resource": "user_profile",
          "actions": ["read"]
        }
        """
        role = request.data["role"]
        resource = request.data["resource"]
        actions = request.data["actions"]

        PERMISSIONS.setdefault(role, {})[resource] = actions

        return Response(PERMISSIONS)