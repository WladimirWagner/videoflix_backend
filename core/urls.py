from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('videoflix_app.api.urls')),
    path('api/', include('auth_app.api.urls')),
    path('api/', include('rest_framework.urls')),
]

# Debug Toolbar URLs (nur im Debug-Modus)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
