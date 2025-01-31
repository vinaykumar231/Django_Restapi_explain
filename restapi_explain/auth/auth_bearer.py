import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
from .auth_handler import decodeJWT
from user.models import AriyanspropertiesUser


class JWTBearer:
    """
    JWT authentication class for extracting and validating the token.
    """

    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error

    def __call__(self, request):
        token = self.extract_token(request)
        if token:
            user_data = decodeJWT(token)
            if user_data:
                return user_data  # Return the decoded data (user information)
            else:
                return JsonResponse({"detail": "Invalid or expired token"}, status=403)
        else:
            return JsonResponse({"detail": "Authorization token is missing"}, status=403)

    def extract_token(self, request):
        """
        Extracts the JWT token from the Authorization header.
        """
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                return parts[1]
        return None


# Decorators for role-based access control (Admin, HR, etc.)
def get_user_from_token(request):
    token = JWTBearer()(request)
    if isinstance(token, JsonResponse):  # If a JsonResponse is returned, it indicates an error
        return token
    return token.get("user_id")

def get_current_user(request):
    """
    Utility function to get the current user from the JWT token.
    """
    token = JWTBearer()(request)
    if isinstance(token, JsonResponse):  # If a JsonResponse is returned, it indicates an error
        return token
    user_id = token.get("user_id")
    if user_id:
        user = AriyanspropertiesUser.objects.filter(user_id=user_id).first()
        if user:
            return user
    return JsonResponse({"detail": "User not found or invalid token"}, status=404)


def login_required(view_func):
    """
    Decorator to enforce that the user must be authenticated.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user_data = JWTBearer()(request)
        if isinstance(user_data, JsonResponse):  # If token is invalid or missing
            return user_data
        request.user_data = user_data
        return view_func(request, *args, **kwargs)

    return wrapped_view


def admin_required(view_func):
    """
    Decorator to enforce that the user must be an admin.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user_data = JWTBearer()(request)
        if isinstance(user_data, JsonResponse):  # If token is invalid or missing
            return user_data

        user_id = user_data.get("user_id")
        user = AriyanspropertiesUser.objects.filter(user_id=user_id).first()
        if user is None or user.user_type != "admin":
            return JsonResponse({"error": "Forbidden: Admin access required"}, status=403)
        
        request.user = user  # Attach user to the request
        return view_func(request, *args, **kwargs)

    return wrapped_view


def hr_required(view_func):
    """
    Decorator to enforce that the user must be HR.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user_data = JWTBearer()(request)
        if isinstance(user_data, JsonResponse):  # If token is invalid or missing
            return user_data

        user_id = user_data.get("user_id")
        user = AriyanspropertiesUser.objects.filter(user_id=user_id).first()
        if user is None or user.user_type != "user":
            return JsonResponse({"error": "Forbidden: HR access required"}, status=403)

        request.user = user  # Attach user to the request
        return view_func(request, *args, **kwargs)

    return wrapped_view


def admin_or_user_required(view_func):
    """
    Decorator to enforce that the user must be either an Admin or HR.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user_data = JWTBearer()(request)
        if isinstance(user_data, JsonResponse):  # If token is invalid or missing
            return user_data

        user_id = user_data.get("user_id")
        user = AriyanspropertiesUser.objects.filter(user_id=user_id).first()
        if user is None or user.user_type not in ["user", "admin"]:
            return JsonResponse({"error": "Forbidden: Admin or HR access required"}, status=403)

        request.user = user  # Attach user to the request
        return view_func(request, *args, **kwargs)

    return wrapped_view

