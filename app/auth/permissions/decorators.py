from rest_framework.response import Response
from rest_framework import status
from functools import wraps

from .utils import has_permission

def is_admin(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        if not user:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if user.role != "admin":
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return func(self, request, *args, **kwargs)
    return wrapper

def permission_check(resource, action):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not request.user:
                return Response(
                    {"detail": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not has_permission(request.user, resource, action):
                return Response(
                    {"detail": "Forbidden"},
                    status=status.HTTP_403_FORBIDDEN
                )

            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator