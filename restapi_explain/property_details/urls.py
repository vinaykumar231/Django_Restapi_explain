from django.urls import path
from . import views

urlpatterns = [
    path('add_property_details/', views.add_property_details, name='add_property_details'),
    path('get_property_details/', views.get_property_details, name='get_property_details'),
    path('update/<int:id>', views.update_property_details, name='update_property_details'),
    path('delete/<int:id>', views.delete_property_details, name='delete_property_details'),
    path('get/<int:id>', views.get_property_details_by_id, name='get_property_details_by_id'),
]
