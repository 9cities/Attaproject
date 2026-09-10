from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Landing Page
    path("", include("home.urls")),

    # Akun
    path("", include("akun.urls")),

    # Ujian
    path("", include("ujian.urls")),

    # Import
    path("", include("importer.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)