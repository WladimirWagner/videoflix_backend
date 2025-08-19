from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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

# Media files (für Thumbnails und Videos)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
