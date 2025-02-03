from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),  # Ensure this includes 'user.urls'
    path('api/', include('property_data.urls')),
    path('api/', include('property_details.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
