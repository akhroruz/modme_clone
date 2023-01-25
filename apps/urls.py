from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import RoleModelViewSet, BranchModelViewSet

router = DefaultRouter()
router.register('role', RoleModelViewSet, basename='role')
router.register('branch', BranchModelViewSet, basename='branch')
urlpatterns = [
    path('', include(router.urls))
]
