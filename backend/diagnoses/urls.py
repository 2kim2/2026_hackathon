from django.urls import path

from .views import (
    DiagnosisResultListCreateView,
    DiagnosisResultDetailView,
)


urlpatterns = [

    # 진단 결과 등록 및 목록 조회
    path(
        '',
        DiagnosisResultListCreateView.as_view(),
        name='diagnosis-list-create'
    ),

    # 진단 결과 상세 조회
    path(
        '<int:pk>/',
        DiagnosisResultDetailView.as_view(),
        name='diagnosis-detail'
    ),

]