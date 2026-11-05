from django.urls import path
from .views import test_api, analyze_snapshot

urlpatterns = [
    path('test/', test_api),
    path('analyze/',analyze_snapshot),
]