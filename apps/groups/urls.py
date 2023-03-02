from django.urls import path, include
from rest_framework.routers import DefaultRouter

from groups.views import GroupModelViewSet, BranchModelViewSet, RoomModelViewSet, HomeListAPIView
from groups.views.views import CompanyModelViewSet, CourseModelViewSet, HolidayModelViewSet

router = DefaultRouter()
router.register('group', GroupModelViewSet, 'group')
router.register('branch', BranchModelViewSet, 'branch')
router.register('room', RoomModelViewSet, 'room')
router.register('company', CompanyModelViewSet, 'company')
router.register('course', CourseModelViewSet, 'course')
router.register('holiday', HolidayModelViewSet, 'holiday')
# router.register('archive-reasons', ArchiveReasonsModelViewSet, 'archive_reasons')

urlpatterns = [
    path('home', HomeListAPIView.as_view(), name='home'),
    path('', include(router.urls)),
]
