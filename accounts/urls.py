from django.urls import path

from .views import (
    RegistrationAPIView, LoginAPIView, LogoutAPIView
)

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
