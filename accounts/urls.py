from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    UserProfileView,
)


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # 내 정보
    path('me/', UserProfileView.as_view(), name='my-profile'),
]