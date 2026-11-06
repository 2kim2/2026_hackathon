from django.urls import path
from .views import FCMTokenView

urlpatterns = [
    path('fcm-token/', FCMTokenView.as_view(), name='fcm-token'),
]
