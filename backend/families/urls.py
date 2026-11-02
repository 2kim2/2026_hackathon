
from django.urls import path

from .views import (
    FamilyConnectionCodeCreateView,
    FamilyRequestByCodeView,
    FamilyRequestView,
    FamilyRequestListView,
    FamilyResponseView,
    FamilyConnectionListView,
)


urlpatterns = [
    # 어르신의 연결 코드 생성
    path(
        'codes/',
        FamilyConnectionCodeCreateView.as_view(),
        name='family-code-create'
    ),

    # 보호자의 연결 코드 입력 및 연결 요청
    path(
        'requests/by-code/',
        FamilyRequestByCodeView.as_view(),
        name='family-request-by-code'
    ),

    # 기존 보호자의 아이디 기반 연결 요청
    path(
        'requests/',
        FamilyRequestView.as_view(),
        name='family-request'
    ),

    # 어르신이 받은 요청 확인
    path(
        'requests/received/',
        FamilyRequestListView.as_view(),
        name='family-request-list'
    ),

    # 연결 요청 수락 또는 거절
    path(
        'requests/<int:connection_id>/respond/',
        FamilyResponseView.as_view(),
        name='family-response'
    ),

    # 연결된 가족 목록
    path(
        'connections/',
        FamilyConnectionListView.as_view(),
        name='family-connection-list'
    ),
]
