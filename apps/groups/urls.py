from django.urls import path, include
from rest_framework.routers import DefaultRouter

from groups.views.groups import GroupModelViewSet
from groups.views.views import BranchModelViewSet, RoomModelViewSet, CourseModelViewSet, RoleModelViewSet

router = DefaultRouter()
router.register('role', RoleModelViewSet, basename='role')
router.register('course', CourseModelViewSet, basename='course')
router.register('group', GroupModelViewSet, basename='group')
# router.register('weekend', WeekendModelViewSet, basename='weekend')
# router.register('group', GroupModelViewSet, basename='group')
router.register('branch', BranchModelViewSet, basename='branch')
router.register('room', RoomModelViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]
