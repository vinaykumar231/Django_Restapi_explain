from django.contrib import admin
from .models import AriyanspropertiesUser

# Optionally, create a custom admin class to modify how the model appears in the admin interface
class AriyanspropertiesUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_email', 'user_type', 'created_on')  # Columns to show in the list view
    search_fields = ('user_name', 'user_email')  # Fields to search by
    list_filter = ('user_type',)  # Filter by user type
    ordering = ('created_on',)  # Order by creation date

# Register your models here
admin.site.register(AriyanspropertiesUser, AriyanspropertiesUserAdmin)
