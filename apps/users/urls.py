from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import UserModelViewSet, RegisterView

from django.urls import path
from users.views import MyObtainTokenPairView

router = DefaultRouter()
router.register('user', UserModelViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),

]
