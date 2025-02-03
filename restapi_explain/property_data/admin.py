# property/admin.py

from django.contrib import admin
from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'property_code', 
        'user_id', 
        'building', 
        'address2', 
        'city', 
        'area', 
        'pin', 
        'des_code', 
        'lease_code', 
        'status_code', 
        'usp', 
        'company', 
        'contact_person1', 
        'contact_person2', 
        'contact_person3', 
        'c_status', 
        'property_type'
    )  # Displaying the property fields in the admin list view
    search_fields = ['building', 'user_id__user_name', 'city', 'area']  # Search functionality
    list_filter = ['property_type', 'status_code', 'city']  # Filters on the right side of the list view

admin.site.register(Property, PropertyAdmin)
