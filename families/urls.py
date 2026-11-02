from django.urls import path

from .views import (
    FamilyRequestView,
    FamilyRequestListView,
    FamilyResponseView,
    FamilyConnectionListView,
)


urlpatterns = [
    # 보호자의 연결 요청
    path('requests/', FamilyRequestView.as_view()),

    # 어르신이 받은 요청 확인
    path('requests/received/', FamilyRequestListView.as_view()),

    # 연결 요청 수락 또는 거절
    path(
        'requests/<int:connection_id>/respond/',
        FamilyResponseView.as_view()
    ),

    # 연결된 가족 목록
    path('connections/', FamilyConnectionListView.as_view()),
]