# property/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.get_all_properties, name='get_all_properties'),  # Get all properties
    path('properties/<int:property_code>/', views.get_property_by_id, name='get_property_by_id'),  # Get a property by ID
    path('properties/create/', views.create_property, name='create_property'),  # Create a new property
    path('properties/update/<int:property_code>/', views.update_property, name='update_property'),  # Update a property
    path('properties/delete/<int:property_code>/', views.delete_property, name='delete_property'),  # Delete a property
]
