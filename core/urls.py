from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core import settings

schema_view = get_schema_view(
    openapi.Info(
        title="ModMe API",
        default_version='v1',
        description="Backend API for ModMe",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="modme@service"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include('apps.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
