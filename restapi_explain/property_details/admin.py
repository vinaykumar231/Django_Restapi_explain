from django.contrib import admin
from .models import PropertyDetails

class PropertyDetailsAdmin(admin.ModelAdmin):
    # Define which fields to display in the admin list view
    list_display = ('property_code', 'rate_buy', 'rate_lease', 'floor', 'unit_no', 'wing', 'car_parking', 'remarks', 'edit_date', 'user_id')

    # Make fields searchable in the admin
    search_fields = ('property_code', 'unit_no', 'wing')

    # Add filters in the sidebar for better filtering of records
    list_filter = ('floor', 'rate_buy', 'rate_lease', 'car_parking', 'user_id')

    # Allow adding, editing, or deleting PropertyDetails directly in the admin interface
    fields = ('property_code', 'property_image_path', 'rate_buy', 'rate_lease', 'floor', 'unit_no', 'wing', 'car_parking', 'remarks', 'edit_date', 'user_id')

    # You can also specify how the list will be ordered by default
    ordering = ('-edit_date',)

admin.site.register(PropertyDetails, PropertyDetailsAdmin)
