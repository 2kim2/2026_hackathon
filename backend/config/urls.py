from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # 사용자 인증 API
    path('api/accounts/', include('accounts.urls')),

    # 가족 연결 API
    path('api/families/', include('families.urls')),

    # 설치 앱 정보 API
    path('api/applications/', include('applications.urls')),

    # 진단 결과 API
    path('api/diagnoses/', include('diagnoses.urls')),
    
    # FCM 토큰 관리 API
    path('api/notifications/', include('notifications.urls')),
]