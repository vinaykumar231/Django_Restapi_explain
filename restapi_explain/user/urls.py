from django.urls import path
from .views import register, login, get_all_users, get_user_by_id, update_user, delete_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('users/', get_all_users, name='get_all_users'),  # Get all users
    path('users/<int:user_id>/', get_user_by_id, name='get_user_by_id'),  # Get user by ID
    path('users/<int:user_id>/update/', update_user, name='update_user'),  # Update user
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),  # Delete user
]
