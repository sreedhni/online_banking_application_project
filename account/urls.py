from django.urls import path
from account.views import UserRegistrationAPIView, UserLoginView, StaffRegistrationAPIView,LogoutAPIView

urlpatterns = [
    path(
        'register/',
        UserRegistrationAPIView.as_view(),
        name='register',
    ),
    path(
        'login/',
        UserLoginView.as_view(),
        name='login',
    ),
    path(
        'staffregister/',
        StaffRegistrationAPIView.as_view(),
        name='staff-register',
    ),

    path('logout/',
          LogoutAPIView.as_view(),
          name='logout'),
]
