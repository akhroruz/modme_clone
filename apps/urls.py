from django.urls import path, include

urlpatterns = [
    path('', include('groups.urls')),
    path('', include('users.urls')),
    path('', include('crm.urls')),
    path('', include('payments.urls')),
]
